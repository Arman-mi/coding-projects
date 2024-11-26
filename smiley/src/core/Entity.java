package core;

import tileengine.TETile;
import tileengine.Tileset;

// im just calling it entity cause y not? it could also be baaaaad guuuuuuyyyyyyyys
// if the bad guys catch you your computer will break and you will get blue screen of death!!!!!

    public class Entity {
        int x, y;
        TETile tile;
        int health;
        int damage;

        public Entity(int x, int y, TETile tile) {
            this.x = x;
            this.y = y;
            this.tile = tile;
            this.health = 50;
            this.damage = 10;
        }

        public void takeDamage(int amount) {
            health -= amount;
        }

        public boolean isAlive() {
            return health > 0;
        }

        public void moveTowards(int targetX, int targetY, TETile[][] world) {
            int dx = Integer.compare(targetX, x);
            int dy = Integer.compare(targetY, y);

            if (dx != 0 && world[x + dx][y] != Tileset.WALL && world[x + dx][y] != Tileset.CELL) {
                x += dx;
            } else if (dy != 0 && world[x][y + dy] != Tileset.WALL && world[x][y + dy] != Tileset.CELL) {
                y += dy;
            }
        }
    }






