#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <curses.h>

const int GRID_SIZE = 25;
const int TOPPLING_COUNT = 4;
const char GRAINS_0 = ' ';
const char GRAINS_1 = '.';
const char GRAINS_2 = 'o';
const char GRAINS_3 = 'O';
const char GRAINS_4 = '@';
const int FRAME_RATE_NS = 100;

typedef struct gridTile {
  int x;
  int y;
} gridTile;

int generateRandom(int range) {
  //TODO: use sodium's func to find random
  return rand() % range;
}

void addGrain(int grid[GRID_SIZE][GRID_SIZE]) {
  grid[generateRandom(GRID_SIZE)][generateRandom(GRID_SIZE)] += 1;
}

void initGrid(int grid[GRID_SIZE][GRID_SIZE]) {
  for (int i = 0; i < GRID_SIZE; i++) {
    for (int j = 0; j < GRID_SIZE; j++) {
      grid[i][j] = generateRandom(TOPPLING_COUNT);
    }
  }
}

int checkIfUnstableAndSetTile(int grid[GRID_SIZE][GRID_SIZE], gridTile *tilePtr) {
  for (int i = 0; i < GRID_SIZE; i++) {
    for (int j = 0; j < GRID_SIZE; j++) {
      if (grid[i][j] >= TOPPLING_COUNT) {
        tilePtr->x = j;
        tilePtr->y = i;
        return 1;
      }
    }
  }
  return 0;
}

void topple(int grid[GRID_SIZE][GRID_SIZE], gridTile *tilePtr){
  if (tilePtr->x >= 1){
    grid[tilePtr->y][tilePtr->x-1] += 1;
  }
  if (tilePtr->x <= GRID_SIZE-2){
    grid[tilePtr->y][tilePtr->x+1] += 1;
  }
  if (tilePtr->y >= 1){
    grid[tilePtr->y-1][tilePtr->x] += 1;
  }
  if (tilePtr->y <= GRID_SIZE-2){
    grid[tilePtr->y+1][tilePtr->x] += 1;
  }
  grid[tilePtr->y][tilePtr->x] -= 4;
}

void mapGrid(int grid[GRID_SIZE][GRID_SIZE], char gridVisu[]) {
  for (int i = 0; i <= GRID_SIZE; i++) {
    for (int j = 0; j <= GRID_SIZE; j++) {
      if (i == GRID_SIZE) {
        gridVisu[i*GRID_SIZE + i + j] = '\0';
        break;
      }
      if (j == GRID_SIZE) {
        gridVisu[i*GRID_SIZE + i + j]= '\n';
        }        
      else {
        switch (grid[i][j]) {
          case 0:
            gridVisu[i*GRID_SIZE + i + j] = GRAINS_0;
            break;
          case 1:
            gridVisu[i*GRID_SIZE + i + j] = GRAINS_1;
            break;
          case 2:
            gridVisu[i*GRID_SIZE + i + j] = GRAINS_2;
            break;
          case 3:
            gridVisu[i*GRID_SIZE + i + j] = GRAINS_3;
            break;
          default:
            gridVisu[i*GRID_SIZE + i + j] = GRAINS_4;
        }
      }
    }
  }
}

void printVisu(int grid[GRID_SIZE][GRID_SIZE], char gridVisu[]) {
  mapGrid(grid, gridVisu);
  erase();
  printw("%s", gridVisu);
  refresh();
  napms(FRAME_RATE_NS);
}

int main() { 
  time_t time_seed;
  int grid[GRID_SIZE][GRID_SIZE];
  char gridVisu[(GRID_SIZE + 1) * GRID_SIZE + 1];
  gridTile tile;
  gridTile *tilePtr = &tile;
  // Set rand() seed
  srand((unsigned) time(&time_seed));

  // Start simulation
  initscr();
  initGrid(grid);
  printVisu(grid, gridVisu);
  while (1) {
    addGrain(grid);
    printVisu(grid, gridVisu);
    while (checkIfUnstableAndSetTile(grid, tilePtr)) {
      topple(grid, tilePtr);
      printVisu(grid, gridVisu);
    }
  }
  endwin();
  return 0;
}

