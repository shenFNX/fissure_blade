package com.shen.fissureblade;

import net.minecraft.core.component.DataComponents;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.resources.ResourceKey;
import net.minecraft.core.registries.Registries;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

import net.minecraft.world.item.Rarity;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;

public class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(FissureBlade.MODID);

    private static final ResourceKey<Item> FISSURE_BLADE_KEY = ResourceKey.create(Registries.ITEM, Identifier.parse(FissureBlade.MODID + ":fissure_blade"));
    private static final ResourceKey<Item> FISSURE_BLADE_CORE_KEY = ResourceKey.create(Registries.ITEM, Identifier.parse(FissureBlade.MODID + ":fissure_blade_core"));

    public static final DeferredItem<Item> FISSURE_BLADE_CORE = ITEMS.register("fissure_blade_core", () -> new Item(new Item.Properties()
            .setId(FISSURE_BLADE_CORE_KEY)
            .stacksTo(64)
    ));

    public static final DeferredItem<Item> FISSURE_BLADE = ITEMS.register("fissure_blade", () -> new Item(new Item.Properties()
            .setId(FISSURE_BLADE_KEY)
            .stacksTo(1)
            .durability(512)
            .component(DataComponents.ITEM_NAME, Component.translatable("item.fissure_blade.fissure_blade").withStyle(ChatFormatting.DARK_PURPLE))
            .component(DataComponents.ATTRIBUTE_MODIFIERS, ItemAttributeModifiers.builder()
                    .add(Attributes.ATTACK_DAMAGE, new AttributeModifier(
                            Identifier.parse("fissure_blade:attack_damage"), 
                            232.0, // Base 1 + 232 = 233
                            AttributeModifier.Operation.ADD_VALUE), 
                            EquipmentSlotGroup.MAINHAND)
                    .add(Attributes.ATTACK_SPEED, new AttributeModifier(
                            Identifier.parse("fissure_blade:attack_speed"), 
                            -3.0, // Base 4 - 3 = 1
                            AttributeModifier.Operation.ADD_VALUE), 
                            EquipmentSlotGroup.MAINHAND)
                    .build())
    ));
}
