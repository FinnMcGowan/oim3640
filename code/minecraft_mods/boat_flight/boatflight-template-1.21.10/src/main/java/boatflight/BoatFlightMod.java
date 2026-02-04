package com.yourname.boatflight;  // Change to your package

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import net.minecraft.entity.vehicle.BoatEntity;
import net.minecraft.text.Text;
import net.minecraft.util.math.Vec3d;
import org.lwjgl.glfw.GLFW;

/**
 * Client-side Fabric mod that adds toggleable boat flight.
 * Works on vanilla servers by controlling boat velocity client-side.
 * 
 * Features:
 * - Toggle flight with B (default)
 * - Adjust speed with I (increase) / O (decrease)
 * - Fly in the direction you're looking (WASD)
 * - Ascend/descend with Space / Shift
 * - Hover when no vertical input
 * 
 * WARNING: High speeds may cause server kick or rubber-banding on vanilla.
 * Keep flightSpeed around 0.2–0.5 for smooth play.
 */
public class BoatFlightMod implements ClientModInitializer {

    // Keybindings (configurable in Controls menu)
    private static KeyBinding toggleKey;
    private static KeyBinding increaseSpeedKey;
    private static KeyBinding decreaseSpeedKey;

    // State variables
    private static boolean flightEnabled = false;
    private static float flightSpeed = 0.3f;      // Horizontal speed (blocks/tick). ~6 blocks/second at 0.3.
    private static final float VERTICAL_SPEED = 0.25f;  // Up/down speed
    private static final float SPEED_STEP = 0.05f;      // How much speed changes per press

    @Override
    public void onInitializeClient() {
        // Register keybindings – these appear in Minecraft's Controls menu
        // Category helps group them under "Boat Flight" in the menu
        toggleKey = KeyBindingHelper.registerKeyBinding(new KeyBinding(
                "key.boatflight.toggle",
                InputUtil.Type.KEYSYM,
                GLFW.GLFW_KEY_B,
                "key.categories.boatflight"
        ));

        increaseSpeedKey = KeyBindingHelper.registerKeyBinding(new KeyBinding(
                "key.boatflight.increase",
                InputUtil.Type.KEYSYM,
                GLFW.GLFW_KEY_I,
                "key.categories.boatflight"
        ));

        decreaseSpeedKey = KeyBindingHelper.registerKeyBinding(new KeyBinding(
                "key.boatflight.decrease",
                InputUtil.Type.KEYSYM,
                GLFW.GLFW_KEY_O,
                "key.categories.boatflight"
        ));

        // Hook into every client tick (runs 20 times/second)
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            MinecraftClient mc = MinecraftClient.getInstance();  // Shortcut to client instance

            // Handle toggle key presses (while loop drains repeated presses)
            while (toggleKey.wasPressed()) {
                flightEnabled = !flightEnabled;
                if (mc.player != null) {
                    mc.player.sendMessage(
                            Text.literal("Boat Flight " + (flightEnabled ? "§aENABLED" : "§cDISABLED")),
                            false  // false = action bar (not chat)
                    );
                }
            }

            // Handle speed adjustment keys
            while (increaseSpeedKey.wasPressed()) {
                flightSpeed += SPEED_STEP;
                sendSpeedMessage(mc);
            }
            while (decreaseSpeedKey.wasPressed()) {
                flightSpeed = Math.max(0.05f, flightSpeed - SPEED_STEP);  // Prevent negative/zero speed
                sendSpeedMessage(mc);
            }

            // Only proceed if player exists and is riding a boat
            if (mc.player == null || !(mc.player.getVehicle() instanceof BoatEntity boat)) {
                return;
            }

            if (flightEnabled) {
                // Disable gravity so the boat doesn't fall (client prediction only)
                boat.setNoGravity(true);

                // Get player movement inputs
                boolean pressingForward = mc.options.forwardKey.isPressed();
                boolean pressingBack = mc.options.backKey.isPressed();
                boolean pressingLeft = mc.options.leftKey.isPressed();
                boolean pressingRight = mc.options.rightKey.isPressed();
                boolean pressingJump = mc.options.jumpKey.isPressed();
                boolean pressingSneak = mc.options.sneakKey.isPressed();

                // Calculate horizontal movement direction based on where player is looking
                Vec3d horizontalVelocity = Vec3d.ZERO;
                if (pressingForward || pressingBack || pressingLeft || pressingRight) {
                    Vec3d lookDirection = mc.player.getRotationVector();  // Unit vector where player is facing

                    if (pressingForward) {
                        horizontalVelocity = horizontalVelocity.add(lookDirection.multiply(flightSpeed));
                    }
                    if (pressingBack) {
                        horizontalVelocity = horizontalVelocity.add(lookDirection.multiply(-flightSpeed));
                    }

                    // Strafe perpendicular to look direction
                    Vec3d strafeDirection = lookDirection.rotateY((float) Math.toRadians(90));  // 90 degrees right
                    if (pressingLeft) {
                        horizontalVelocity = horizontalVelocity.add(strafeDirection.multiply(flightSpeed));
                    }
                    if (pressingRight) {
                        horizontalVelocity = horizontalVelocity.add(strafeDirection.multiply(-flightSpeed));
                    }
                }

                // Vertical movement (jump to rise, shift to descend; no input = hover)
                double vertical = 0.0;
                if (pressingJump) vertical += VERTICAL_SPEED;
                if (pressingSneak) vertical -= VERTICAL_SPEED;

                // Combine into final velocity
                Vec3d finalVelocity = new Vec3d(horizontalVelocity.x, vertical, horizontalVelocity.z);

                // Apply velocity to boat
                boat.setVelocity(finalVelocity);

                // Sync boat rotation with player so it faces the way you're looking
                boat.setYaw(mc.player.getYaw());
                boat.setPitch(mc.player.getPitch());
            } else {
                // Re-enable gravity when flight is off (important for normal boat behavior)
                boat.setNoGravity(false);
            }
        });
    }

    // Helper to show current speed in action bar
    private static void sendSpeedMessage(MinecraftClient mc) {
        if (mc.player != null) {
            mc.player.sendMessage(
                    Text.literal("Boat Flight Speed: §e" + String.format("%.2f", flightSpeed)),
                    false
            );
        }
    }
}