package core;

import tileengine.TETile;
import tileengine.Tileset;

import java.awt.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class World implements Serializable {
    private final int WIDTH;
    private final int HEIGHT;
    private final Random RANDOM;
    private TETile[][] world;
    private final int MAX_ATTEMPTS = 1000;
// for the avatar
    private int avatarX;
    private int avatarY;
    private final int MAX_ROOMS = 20;
    private List<Entity> entities;

    //new start//
    private int playerHealth;
    private static final int MAX_PLAYER_HEALTH = 100;
    private static final int HEALTH_POTION_RESTORE = 20;
    private List<Point> healthPotions;
    private int roundNumber;
    private static final int INITIAL_HEALTH_POTIONS = 5;
    private static final int INITIAL_ENTITIES = 1;
    //new end//

    public World(int width, int height, long seed) {
        this.WIDTH = width;
        this.HEIGHT = height;
        this.RANDOM = new Random(seed);
        this.world = new TETile[WIDTH][HEIGHT];
        this.entities = new ArrayList<>();
        //new start//
        this.playerHealth = MAX_PLAYER_HEALTH;
        this.healthPotions = new ArrayList<>();
        this.roundNumber = 1;
        //new end//
    }

    public void generateWorld() {
        // Initialize world with NOTHING tiles
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                world[x][y] = Tileset.NOTHING;
            }
        }
// there are bugs here kelly im changing the code so it runs.

        // so the code here you were adding the potions to the world twice, once when
        // making the world and once when starting the round,
        //this caused java to shit itself when I tried reloading it because it reloaded with the world
        // it was saving not the extra ones so when you reloaded you had 5 less potions.
        // i fixed that here
        List<Room> rooms = generateRooms();
        connectRooms(rooms);
        addWalls();
        placeAvatar(); // this places the avatar in the world
        placeEntities(1);
        //new start//
       // placeHealthPotions(INITIAL_HEALTH_POTIONS);
        startNewRound();
        //new end//
    }

    //new start//
    private void startNewRound() {
        clearEntities();
        placeEntities(INITIAL_ENTITIES + roundNumber - 1);
        placeHealthPotions(INITIAL_HEALTH_POTIONS);
        System.out.println("Round " + roundNumber + " started!");
    }

    private void clearEntities() {
        for (Entity entity : entities) {
            world[entity.x][entity.y] = Tileset.FLOOR;
        }
        entities.clear();
    }

    public void placeHealthPotions(int count) {
        healthPotions.clear();
        for (int i = 0; i < count; i++) {
            int x, y;
            do {
                x = RANDOM.nextInt(WIDTH);
                y = RANDOM.nextInt(HEIGHT);
            } while (world[x][y] != Tileset.FLOOR);
            world[x][y] = Tileset.HEART;
            healthPotions.add(new Point(x, y));
        }
    }

    public void checkForRoundEnd() {
        if (entities.isEmpty()) {
            roundNumber++;
            startNewRound();
        }
    }
    //new end//

    private void placeEntities(int count) {
        for (int i = 0; i < count; i++) {
            while (true) {
                int x = RANDOM.nextInt(WIDTH);
                int y = RANDOM.nextInt(HEIGHT);
                if (world[x][y] == Tileset.FLOOR) {
                    entities.add(new Entity(x, y, Tileset.CELL));
                    world[x][y] = Tileset.CELL;  // Set entity position
                    break;
                }
            }
        }
    }

    public void moveEntities() {
        for (Entity entity : entities) {
            world[entity.x][entity.y] = Tileset.FLOOR;  // Clear old position
            entity.moveTowards(avatarX, avatarY, world);
            world[entity.x][entity.y] = entity.tile;  // Update new position
        }
    }

    public boolean checkCollision() {
        for (Entity entity : entities) {
            if (entity.x == avatarX && entity.y == avatarY) {
//                return true;
                //new start//
                playerHealth -= 5; // Player takes 10 damage on collision
                System.out.println("Ouch! Health reduced to " + playerHealth);
                if (playerHealth <= 0) {
                    System.out.println("Game Over! You ran out of health.");
                    return true;
                }
                // Move the player away from the entity
                moveAvatarAway(entity);
                return false;
                //new end//
            }
        }
        return false;
    }

    public void addEntity() {
        placeEntities(1);  // Add one more entity
    }



    //Arman is adding this method
    private void placeAvatar() {
        while (true) {
            int x = RANDOM.nextInt(WIDTH);
            int y = RANDOM.nextInt(HEIGHT);
            if (world[x][y] == Tileset.FLOOR) {
                avatarX = x;
                avatarY = y;
                world[avatarX][avatarY] = Tileset.AVATAR;
                break;
            }
        }
    }

    // this is how bro moves in the world, hopefully he does (skeleton emoji)

    public void moveAvatar(char direction) {
        int newX = avatarX;
        int newY = avatarY;

        switch (direction) {
            case 'w':
                newY += 1;
                break;
            case 'a':
                newX -= 1;
                break;
            case 's':
                newY -= 1;
                break;
            case 'd':
                newX += 1;
                break;
        }
        if (newX >= 0 && newX < WIDTH && newY >= 0 && newY < HEIGHT && world[newX][newY] != Tileset.WALL) {
            world[avatarX][avatarY] = Tileset.FLOOR; // Replace the old position with a floor tile
            avatarX = newX;
            avatarY = newY;
            world[avatarX][avatarY] = Tileset.AVATAR; // Set the new position to the avatar
        }
        //new start//
        checkForHealthPotion();
        //new end//
    }

    //new start//
    private void checkForHealthPotion() {
        Point avatarPos = new Point(avatarX, avatarY);
        if (healthPotions.remove(avatarPos)) {
            playerHealth = Math.min(MAX_PLAYER_HEALTH, playerHealth + HEALTH_POTION_RESTORE);
            System.out.println("Health restored! Current health: " + playerHealth);
        }
    }
    //new end//

    private List<Room> generateRooms() {
        List<Room> rooms = new ArrayList<>();
        int attempts = 0;

        while (rooms.size() < MAX_ROOMS && attempts < MAX_ATTEMPTS) {
            int width = RANDOM.nextInt(3, 8);
            int height = RANDOM.nextInt(3, 8);
            int x = RANDOM.nextInt(1, WIDTH - width - 1);
            int y = RANDOM.nextInt(1, HEIGHT - height - 1);

            Room newRoom = new Room(x, y, width, height);

            if (!overlapsWithExistingRooms(newRoom, rooms)) {
                rooms.add(newRoom);
                for (int i = x; i < x + width; i++) {
                    for (int j = y; j < y + height; j++) {
                        world[i][j] = Tileset.FLOOR;
                    }
                }
            }
            attempts++;
        }

        return rooms;
    }

    //new start//
    private void moveAvatarAway(Entity entity) {
        int dx = avatarX - entity.x;
        int dy = avatarY - entity.y;
        int newX = avatarX + (dx != 0 ? dx / Math.abs(dx) : 0);
        int newY = avatarY + (dy != 0 ? dy / Math.abs(dy) : 0);
        if (newX >= 0 && newX < WIDTH && newY >= 0 && newY < HEIGHT && world[newX][newY] == Tileset.FLOOR) {
            world[avatarX][avatarY] = Tileset.FLOOR;
            avatarX = newX;
            avatarY = newY;
            world[avatarX][avatarY] = Tileset.AVATAR;
        }
    }
    //new end//

    //new start//
    public int getPlayerHealth() {
        return playerHealth;
    }

    public List<Entity> getEntities() {
        return entities;
    }

    public int getAvatarX() {
        return avatarX;
    }

    public int getAvatarY() {
        return avatarY;
    }

    public void removeEntity(Entity entity) {
        entities.remove(entity);
        world[entity.x][entity.y] = Tileset.FLOOR;
    }
    // new end

    private boolean overlapsWithExistingRooms(Room newRoom, List<Room> existingRooms) {
        for (Room room : existingRooms) {
            if (newRoom.overlaps(room)) {
                return true;
            }
        }
        return false;
    }

    private void connectRooms(List<Room> rooms) {
        for (int i = 0; i < rooms.size() - 1; i++) {
            Room room1 = rooms.get(i);
            Room room2 = rooms.get(i + 1);
            connectTwoRooms(room1, room2);
        }
    }

    private void connectTwoRooms(Room room1, Room room2) {
        int x1 = room1.x + RANDOM.nextInt(room1.width);
        int y1 = room1.y + RANDOM.nextInt(room1.height);
        int x2 = room2.x + RANDOM.nextInt(room2.width);
        int y2 = room2.y + RANDOM.nextInt(room2.height);

        // Create L-shaped hallway
        drawHorizontalHallway(Math.min(x1, x2), Math.max(x1, x2), y1);
        drawVerticalHallway(x2, Math.min(y1, y2), Math.max(y1, y2));
    }

    private void drawHorizontalHallway(int x1, int x2, int y) {
        for (int x = x1; x <= x2; x++) {
            world[x][y] = Tileset.FLOOR;
        }
    }

    private void drawVerticalHallway(int x, int y1, int y2) {
        for (int y = y1; y <= y2; y++) {
            world[x][y] = Tileset.FLOOR;
        }
    }

    private void addWalls() {
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                if (world[x][y] == Tileset.FLOOR) {
                    addWallsAroundFloor(x, y);
                }
            }
        }
    }

    private void addWallsAroundFloor(int x, int y) {
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                int newX = x + dx;
                int newY = y + dy;
                if (newX >= 0 && newX < WIDTH && newY >= 0 && newY < HEIGHT) {
                    if (world[newX][newY] == Tileset.NOTHING) {
                        world[newX][newY] = Tileset.WALL;
                    }
                }
            }
        }
    }

// are you a chef? cause you know how to cooooooooooooook!!!
public String getWorldState() {
    StringBuilder sb = new StringBuilder();
    sb.append(WIDTH).append(',').append(HEIGHT).append(',').append(avatarX).append(',').append(avatarY).append(',').append(roundNumber).append('\n');
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            sb.append(world[x][y].character());
        }
        sb.append('\n');
    }
    for (Entity entity : entities) {
        sb.append(entity.x).append(',').append(entity.y).append(',').append(entity.health).append('\n');
    }
    for (Point potion : healthPotions) {
        sb.append(potion.x).append(',').append(potion.y).append('\n');
    }
    return sb.toString();
}

    public static World loadFromString(String worldState) {
        String[] lines = worldState.split("\n");
        String[] params = lines[0].split(",");
        int width = Integer.parseInt(params[0]);
        int height = Integer.parseInt(params[1]);
        int avatarX = Integer.parseInt(params[2]);
        int avatarY = Integer.parseInt(params[3]);
        int roundNumber = Integer.parseInt(params[4]);

        World loadedWorld = new World(width, height, 0);
        loadedWorld.avatarX = avatarX;
        loadedWorld.avatarY = avatarY;
        loadedWorld.roundNumber = roundNumber;

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                char tileChar = lines[y + 1].charAt(x);
                loadedWorld.world[x][y] = charToTile(tileChar);
            }
        }






        loadedWorld.world[avatarX][avatarY] = Tileset.AVATAR;

        int i = height + 1;
        while (i < lines.length) {
            String[] entityParams = lines[i].split(",");
            if (entityParams.length == 3) {




                int entityX = Integer.parseInt(entityParams[0]);
                int entityY = Integer.parseInt(entityParams[1]);
                int entityHealth = Integer.parseInt(entityParams[2]);
                Entity entity = new Entity(entityX, entityY, Tileset.CELL);
                entity.health = entityHealth;
                loadedWorld.entities.add(entity);


                loadedWorld.world[entityX][entityY] = Tileset.CELL;
            } else if (entityParams.length == 2) {

                int potionX = Integer.parseInt(entityParams[0]);
                int potionY = Integer.parseInt(entityParams[1]);
                loadedWorld.healthPotions.add(new Point(potionX, potionY));
                loadedWorld.world[potionX][potionY] = Tileset.HEART;
            }
            i++;
        }

        return loadedWorld;
    }



    public int getRoundNumber() {
        return roundNumber;
    }

    public void setRoundNumber(int roundNumber) {
        this.roundNumber = roundNumber;
    }
// life could be a dream
    // life could be  dreaaam

    //shoo doo do shabi dada




































    public TETile[][] getWorld() {
        return world;
    }

    private static TETile charToTile(char c) {
        switch (c) {
            case '#': return Tileset.WALL;
            case '·': return Tileset.FLOOR;
            case '@': return Tileset.AVATAR;
            case '█': return Tileset.CELL;
            case '♡': return Tileset.HEART;
            default: return Tileset.NOTHING;
        }
    }

    private static class Room {
        int x, y, width, height;

        Room(int x, int y, int width, int height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }

        boolean overlaps(Room other) {
            return this.x < other.x + other.width + 1
                    && this.x + this.width + 1 > other.x
                    && this.y < other.y + other.height + 1
                    && this.y + this.height + 1 > other.y;
        }
    }

}
