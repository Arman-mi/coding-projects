package core;

import tileengine.TERenderer;
import tileengine.TETile;

import java.awt.*;
import edu.princeton.cs.algs4.StdDraw;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;

public class Main {
    public static final int WIDTH = 80;
    static final int HEIGHT = 30;
    private static final int HUD_HEIGHT = 2; // (changed) Added height for the HUD
    private static final int WINDOW_HEIGHT = HEIGHT + HUD_HEIGHT; // (changed) Total height including HUD
    private static final int TITLE_FONT_SIZE = 30;
    private static final int OPTION_FONT_SIZE = 20;
    private TERenderer ter;
    private World currentWorld;
    private long startTime;
    private int round;
    private final int ROUND_DURATION = 30;
    private AudioPlayer audioPlayer;

    public static void main(String[] args) {

        //Armans modifications:
        Main mainInstance = new Main();
        mainInstance.run();
    }

    private void run() {
        ter = new TERenderer();
        ter.initialize(WIDTH, WINDOW_HEIGHT);
        System.out.println(System.getProperty("user.dir"));
        audioPlayer = new AudioPlayer("C:\\Users\\arman>C:\\Users\\arman\\61bl\\proj3\\proj3\\src\\music\\gg.wav");
        audioPlayer.play();

        while (true) {
            drawMainMenu();
            char input = getCharInput();

            switch (input) {
                case 'n':
                    startNewGame();
                    break;
                case 'l':
                    loadGame();
                    break;
                case 'q':
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid input. Please try again.");
            }
        }
    }

    private void drawMainMenu() {
        StdDraw.clear(Color.BLACK);
        StdDraw.setPenColor(Color.WHITE);
        Font titleFont = new Font("Monaco", Font.BOLD, TITLE_FONT_SIZE);
        Font optionFont = new Font("Monaco", Font.PLAIN, OPTION_FONT_SIZE);

        StdDraw.setFont(titleFont);
        StdDraw.text(WIDTH / 2, WINDOW_HEIGHT * 3 / 4, "the Survival of smiley!");

        StdDraw.setFont(optionFont);
        StdDraw.text(WIDTH / 2, WINDOW_HEIGHT / 2, "New Game (N)");
        StdDraw.text(WIDTH / 2, WINDOW_HEIGHT / 2 - 2, "Load Game (L)");
        StdDraw.text(WIDTH / 2, WINDOW_HEIGHT / 2 - 4, "Quit (Q)");

        StdDraw.show();
    }

    private char getCharInput() {
        while (true) {
            if (StdDraw.hasNextKeyTyped()) {
                return Character.toLowerCase(StdDraw.nextKeyTyped());
            }
        }
    }

    private void startNewGame() {
        long seed = getSeed();
        currentWorld = new World(WIDTH, HEIGHT, seed);
        currentWorld.generateWorld();
        //newstart
        startTime = System.currentTimeMillis();
        round = 1;
        //newend
        gameLoop();
    }

    private long getSeed() {
        StdDraw.clear(Color.BLACK);
        StdDraw.setPenColor(Color.WHITE);
        StdDraw.text(WIDTH / 2, WINDOW_HEIGHT / 2, "Enter seed (press S when done):");
        StdDraw.show();

        StringBuilder sb = new StringBuilder();
        while (true) {
            char c = getCharInput();
            if (c == 's') {
                break;
            }
            if (Character.isDigit(c)) {
                sb.append(c);
                StdDraw.clear(Color.BLACK);
                StdDraw.text(WIDTH / 2, WINDOW_HEIGHT / 2, "Seed: " + sb.toString());
                StdDraw.show();
            }
        }
        return Long.parseLong(sb.toString());
    }

    // this game loop method added a couple of years to me, I am offically 33 after going through this
    private void gameLoop() {
        int moveCounter = 0;  // starts the move counter
        final int MOVE_THRESHOLD = 5;  // enemy movement speeeeeeeed,

        while (true) {
            long currentTime = System.currentTimeMillis();
            long elapsedTime = (currentTime - startTime) / 1000;  // Time in seconds
            long remainingTime = ROUND_DURATION - elapsedTime;

            if (elapsedTime >= ROUND_DURATION) {
                round++;
                currentWorld.addEntity();
                startTime = currentTime;  // MR presideent geeeet dowwwwwwn
                // resets the timer
                remainingTime = ROUND_DURATION;
            }

            renderFrameWithHUD(remainingTime);
//            renderFrameWithHUD(currentWorld.getPlayerHealth());

            if (StdDraw.hasNextKeyTyped()) {
                char input = Character.toLowerCase(StdDraw.nextKeyTyped());
                if (input == 'q') {
                    saveGame(currentWorld);
                    System.exit(0);
                }
                if (input == 'w' || input == 'a' || input == 's' || input == 'd') {
                    currentWorld.moveAvatar(input);
                }
                // new start
                if (input == ' ') { // space bar to attack
                    attackNearbyEntities();
                }
                // new end
            }

            moveCounter++;
            if (moveCounter >= MOVE_THRESHOLD) {
                currentWorld.moveEntities();
                moveCounter = 0;  // Reset the counter after moving entities
            }

            if (currentWorld.checkCollision()) {
                System.out.println("Game Over! You were caught.");
                System.exit(0);  // End game if collision occurs
            }

            StdDraw.show();

            // Add a short delay to slow down the game loop
            try {
                Thread.sleep(100);  // can I die now please?
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    // new start
    private void attackNearbyEntities() {
        List<Entity> entities = currentWorld.getEntities();
        int avatarX = currentWorld.getAvatarX();
        int avatarY = currentWorld.getAvatarY();
        List<Entity> entitiesToRemove = new ArrayList<>();

        for (Entity entity : entities) {
            if (Math.abs(entity.x - avatarX) <= 1 && Math.abs(entity.y - avatarY) <= 1) {
                entity.takeDamage(20); // Player deals 20 damage
                System.out.println("You attacked an enemy! Enemy health: " + entity.health);

                if (!entity.isAlive()) {
                    entitiesToRemove.add(entity);
                    System.out.println("Enemy defeated!");
                }
            }
        }

        // Remove defeated entities
        for (Entity entity : entitiesToRemove) {
            currentWorld.removeEntity(entity);
        }
    }
    // new end


    private void renderFrameWithHUD(long remainingTime) {
        StdDraw.clear(Color.BLACK);
        ter.renderFrame(currentWorld.getWorld());

//        drawHUD(remainingTime);
        drawHUD(remainingTime, currentWorld.getPlayerHealth());

        StdDraw.show();
    }

    private void drawHUD(long remainingTime, int playerHealth) {
        int mouseX = (int) StdDraw.mouseX();
        int mouseY = (int) StdDraw.mouseY();

        //new start
        StdDraw.setPenColor(Color.BLACK);
        StdDraw.filledRectangle(WIDTH / 2.0, HEIGHT + 0.5, WIDTH / 2.0, 1);
        StdDraw.setPenColor(Color.WHITE);


        if (mouseX >= 0 && mouseX < WIDTH && mouseY >= 0 && mouseY < HEIGHT) {
            TETile tile = currentWorld.getWorld()[mouseX][mouseY];
            StdDraw.textLeft(1, HEIGHT + 0.5, tile.description());
        }

        // Displays round, time, and health
        StdDraw.textRight(WIDTH - 1, HEIGHT + 0.5, String.format("Round: %d | Time: %ds | Health: %d", round, remainingTime, playerHealth));

    }


// the name is himothy becaue I am HIM


    private void loadGame() {
        try {
            String savedState = Files.readString(Paths.get("savegame.txt"));
            currentWorld = World.loadFromString(savedState);
            startTime = System.currentTimeMillis();
            round = currentWorld.getRoundNumber();
            gameLoop();
        } catch (IOException e) {
            System.out.println("No saved game found.");
        }
    }

    private void saveGame(World world) {
        try {
            world.setRoundNumber(round);
            Files.writeString(Paths.get("savegame.txt"), world.getWorldState());
        } catch (IOException e) {
            System.out.println("Failed to save the game.");
        }
    }

    // I deleted all the commented out versions of save game and load game because it was cluttering my screen since
    //there was waay to many implemntations and none of them were working


    public static TETile[][] getWorldFromInput(String input) {
        input = input.toLowerCase();
        if (input.startsWith("n") && input.endsWith("s")) {
            long seed = Long.parseLong(input.substring(1, input.length() - 1));
            World tempWorld = new World(WIDTH, HEIGHT, seed);
            tempWorld.generateWorld();
            return tempWorld.getWorld();
        }
        return null;
    }


}





