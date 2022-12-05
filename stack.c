#include <stdio.h>
#include <stdlib.h>
#include "stack.h"

stack* initStack(int capacity) {
  stack *ptr = (stack*)malloc(sizeof(stack));
  ptr->maxSize = capacity;
  ptr->top = -1;
  ptr->items = (gridTile*)malloc(sizeof(gridTile) *capacity);
 
  return ptr;
}

int size(stack *ptr) {
  return ptr->top + 1;
}
 
int isEmpty(stack *ptr) {
  return size(ptr) == 0;
}
 
int isFull(stack *ptr) {
  return size(ptr) == ptr->maxSize;
}
 
void push(stack *ptr, gridTile x) {
    if (isFull(ptr)) {
        printf("Overflow\nProgram Terminated\n");
        exit(EXIT_FAILURE);
    }
  pt->items[++pt->top] = x;
}
 
gridTile pop(stack *ptr) {
    if (isEmpty(ptr)) {
      printf("Underflow\nProgram Terminated\n");
      exit(EXIT_FAILURE);
    }
  return ptr->items[ptr->top--];
}