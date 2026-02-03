package com.shen.fissureblade;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;

@EventBusSubscriber(modid = FissureBlade.MODID)
public class FissureBladeEvents {

    private static final String SPLIT_TAG = "fissure_blade_split";

    @SubscribeEvent
    public static void onLivingDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().getEntity() instanceof Player player) {
            if (player.getMainHandItem().is(ModItems.FISSURE_BLADE.get())) {
                if (!(event.getEntity() instanceof Player)) {
                    event.setAmount(10000.0f);
                }
            }
        }
    }

    @SubscribeEvent
    public static void onLivingDeath(LivingDeathEvent event) {
        Entity source = event.getSource().getEntity();
        LivingEntity target = event.getEntity();

        if (source instanceof Player player && player.getMainHandItem().is(ModItems.FISSURE_BLADE.get())) {
            if (target instanceof Player) return;

            if (target.level().isClientSide()) return;
            ServerLevel level = (ServerLevel) target.level();

            double originalMaxHealth = target.getMaxHealth();
            double newMaxHealth = originalMaxHealth / 2.0;

            boolean alreadySplit = target.getPersistentData().contains(SPLIT_TAG);

            boolean isBoss = target.getType() == EntityType.ENDER_DRAGON 
                          || target.getType() == EntityType.WITHER 
                          || target.getType() == EntityType.WARDEN;

            if (newMaxHealth < 2.0 || (isBoss && alreadySplit)) {
                spawnVoidSmoke(level, target);
                return;
            }

            spawnSplitEntities(level, target, newMaxHealth);
        }
    }

    private static void spawnSplitEntities(ServerLevel level, LivingEntity original, double newMaxHealth) {
        for (int i = 0; i < 2; i++) {
            Entity newEntity = original.getType().create(level, EntitySpawnReason.LOAD);
            if (newEntity instanceof LivingEntity livingNewEntity) {
                double offsetX = (i == 0 ? -0.5 : 0.5);
                livingNewEntity.setPos(original.getX() + offsetX, original.getY(), original.getZ() + offsetX);
                
                var healthAttribute = livingNewEntity.getAttribute(Attributes.MAX_HEALTH);
                if (healthAttribute != null) {
                    healthAttribute.setBaseValue(newMaxHealth);
                    livingNewEntity.setHealth((float) newMaxHealth);
                }

                livingNewEntity.getPersistentData().putBoolean(SPLIT_TAG, true);
                level.addFreshEntity(livingNewEntity);
                
                // Use level.addParticle or similar if sendParticles generic fails
                // Or just use a simpler particle type
                try {
                    level.sendParticles(ParticleTypes.LARGE_SMOKE, 
                        livingNewEntity.getX(), livingNewEntity.getY() + 0.5, livingNewEntity.getZ(), 
                        5, 0.2, 0.2, 0.2, 0.05);
                } catch (Exception e) {}
            }
        }
    }

    private static void spawnVoidSmoke(ServerLevel level, LivingEntity entity) {
        try {
            // Using Portal which is usually a SimpleParticleType
            level.sendParticles(ParticleTypes.PORTAL, 
                    entity.getX(), entity.getY() + 1.0, entity.getZ(), 
                    40, 0.5, 0.5, 0.5, 0.2);
        } catch (Exception e) {}
    }
}
