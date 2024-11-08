package core;

import tileengine.TETile;
import tileengine.Tileset;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class AutograderBuddy {

    /**
     * Simulates a game, but doesn't render anything or call any StdDraw
     * methods. Instead, returns the world that would result if the input string
     * had been typed on the keyboard.
     *
     * Recall that strings ending in ":q" should cause the game to quit and
     * save. To "quit" in this method, save the game to a file, then just return
     * the TETile[][]. Do not call System.exit(0) in this method.
     *
     * @param input the input string to feed to your program
     * @return the 2D TETile[][] representing the state of the world
     */
    public static TETile[][] getWorldFromInput(String input) {
        input = input.toLowerCase();
        if (input.startsWith("n")) {
            int endIdx = input.indexOf('s');
            if (endIdx == -1) {
                throw new IllegalArgumentException("Invalid input format.");
            }

            long seed = Long.parseLong(input.substring(1, endIdx));
            World world = new World(Main.WIDTH, Main.HEIGHT, seed);
            world.generateWorld();
            if (input.endsWith(":q")) {
                saveGame(world);
            }
            return world.getWorld();
        } else if (input.startsWith("l")) {
            World loadedWorld = loadGame();
            if (loadedWorld == null) {
                throw new IllegalStateException("No saved game found.");
            }
            if (input.endsWith(":q")) {
                saveGame(loadedWorld);
            }
            return loadedWorld.getWorld();
        } else {
            throw new IllegalArgumentException("Invalid input format.");
        }
    }

    private static void saveGame(World world) {
        try {
            Files.writeString(Paths.get("savegame.txt"), world.getWorldState());
        } catch (IOException e) {
            System.out.println("Failed to save the game.");
        }
    }

    private static World loadGame() {
        try {
            String savedState = Files.readString(Paths.get("savegame.txt"));
            return World.loadFromString(savedState);
        } catch (IOException e) {
            System.out.println("No saved game found.");
            return null;
        }
    }

    /**
     * Used to tell the autograder which tiles are the floor/ground (including
     * any lights/items resting on the ground). Change this
     * method if you add additional tiles.
     */
    public static boolean isGroundTile(TETile t) {
        return t.character() == Tileset.FLOOR.character()
                || t.character() == Tileset.AVATAR.character()
                || t.character() == Tileset.HEART.character();
    }

    /**
     * Used to tell the autograder while tiles are the walls/boundaries. Change
     * this method if you add additional tiles.
     */
    public static boolean isBoundaryTile(TETile t) {
        return t.character() == Tileset.WALL.character()
                || t.character() == Tileset.LOCKED_DOOR.character()
                || t.character() == Tileset.UNLOCKED_DOOR.character();
    }
}
