#ifndef ASM_STACK
#define ASM_STACK

typedef struct gridTile {
  int x;
  int y;
} gridTile;

typedef struct stack {
    int maxSize;
    int top;
    gridTile *items;
}stack;

int size(stack *ptr);
int isEmpty(stack *ptr);
int isFull(stack *ptr);
void push(stack *ptr, gridTile x);
gridTile pop(stack *ptr);

#endif