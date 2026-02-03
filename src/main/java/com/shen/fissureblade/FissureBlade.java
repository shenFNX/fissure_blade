package com.shen.fissureblade;

import org.slf4j.Logger;

import com.mojang.logging.LogUtils;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

@Mod(FissureBlade.MODID)
public class FissureBlade {
    public static final String MODID = "fissure_blade";
    public static final Logger LOGGER = LogUtils.getLogger();
    
    // NOTE: Blocks and Items registries are now in their own classes if needed, 
    // or you can keep them here. But we are cleaning up 'example' stuff.
    // ModItems.ITEMS handles our items. 
    // We will keep CREATIVE_MODE_TABS here for now.

    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    // Creates a creative tab with the id "fissure_blade:general_tab"
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> GENERAL_TAB = CREATIVE_MODE_TABS.register("general_tab", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.fissure_blade")) 
            .withTabsBefore(CreativeModeTabs.COMBAT)
            .icon(() -> ModItems.FISSURE_BLADE.get().getDefaultInstance())
            .displayItems((parameters, output) -> {
                output.accept(ModItems.FISSURE_BLADE.get()); 
                output.accept(ModItems.FISSURE_BLADE_CORE.get());
            }).build());

    public FissureBlade(IEventBus modEventBus, ModContainer modContainer) {
        modEventBus.addListener(this::commonSetup);

        // Register Creative Tabs
        CREATIVE_MODE_TABS.register(modEventBus);
        
        // Register ModItems (which contains our Fissure Blade)
        ModItems.ITEMS.register(modEventBus);

        // Register ourselves for server and other game events we are interested in
        NeoForge.EVENT_BUS.register(this);

        // Register config
        modContainer.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }

    private void commonSetup(FMLCommonSetupEvent event) {

    }

    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
        LOGGER.info("HELLO from server starting");
    }
}