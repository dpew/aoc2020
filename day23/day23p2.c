#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
  int value;
  struct Node *next;
  struct Node *prev;
} Node;

Node **hashmap = NULL;

#define ARRAYSIZE(ARRAY) (sizeof(ARRAY)/sizeof(int))

void
print_cups(Node *nodep) {
  Node *next = nodep;
  do {
    printf("%3d,", next->value); 
    next = next->next;
  } while (next != nodep);
  printf("\n");
}

/*
 * Returns one less than value.  Returned value
 * will always be [1-size]
 */
int
getnext(int value, int size) {
  int newval = (value - 1) % size;
  return (newval == 0) ? size : newval;
}


int
main(int argc, char *argv[]) {

  int puzzle[] = { 3, 6, 2, 9, 8, 1, 7, 5, 4 };
  //int puzzle[] = { 3, 8, 9, 1, 2, 5, 4, 6, 7 };
  int size = ARRAYSIZE(puzzle);
  int iterations = 100;
  int i;

  if (argc > 1) {
     size = atoi(argv[1]);
  }

  if (argc > 2) {
     iterations = atoi(argv[2]);
  }

  for (i = 0; i < ARRAYSIZE(puzzle); i++) {
    //printf("Puzzle[%d] = %d\n", i, puzzle[i]);
  }

  /*
   * Create doubly linked list of elements,
   * put in hashmap.
   */
  hashmap = (Node **)malloc(sizeof(Node *) * size+1);
  Node* lastnode;
  for (i = 0; i < size; i++) {
    Node* node = (Node *)malloc(sizeof(Node));
    if (i < ARRAYSIZE(puzzle)) {
      node->value = puzzle[i];
    } else {
      node->value = i+1;
    }

    if (i == 0) {
      hashmap[0] = node;
    } else {
      node->prev = lastnode;
      lastnode->next = node;
    }
    hashmap[node->value] = node;
    lastnode = node;
  }
  hashmap[0]->prev = lastnode;
  lastnode->next = hashmap[0];

  /** Iterate */
  while (lastnode != hashmap[0]) {
    //printf("Node %d\n", lastnode->value);
    lastnode = lastnode->prev;
  }

  for (i = 0; i <= size; i++) {
    //printf("Node[%d] = %d\n", i, hashmap[i]->value);
  }


  /** Run the program **/
  int nextval;
  Node *current = hashmap[0];
  Node *take[3]; 
  bool match;
  for (i = 0; i < iterations; i++) {
      //print_cups(current);
      nextval = getnext(current->value, size);
      lastnode = current->next;
      match = false;
      for (int p = 0; p < 3; p++) {
         take[p] = lastnode;
         if (lastnode->value == nextval)
           match = true;
         lastnode = lastnode->next;
      }
      /* Move lastnodes */
      current->next = lastnode;
      current->next->prev = current;

      /* If lastnode within our take, find one not in our take */
      while (match) {
        //printf("Matched %d\n", nextval);
        nextval = getnext(nextval, size);
        match = false;
        for (int p = 0; p < 3; p++) {
          if (take[p]->value == nextval) {
            match = true;
          }
          //printf("Matching %d %d %d\n", nextval, take[p]->value, match); 
        }
      }
      //printf("Current %d, nextval %d, takes %d, %d, %d\n", current->value, nextval, take[0]->value, take[1]->value, take[2]->value);

      /* Insert takes into nextval position */
      lastnode = hashmap[nextval];
      take[0]->prev = lastnode;
      take[2]->next = lastnode->next;
      take[0]->prev->next = take[0];
      take[2]->next->prev = take[2];
      current = current->next;
      if (i % 100000 == 0) {
        printf(".");
      }
  }
  //print_cups(current);

  long v1 = hashmap[1]->next->value;
  long v2 = hashmap[1]->next->next->value;
  printf("%d Iterations: After 1: %ld\n", iterations, v1);
  printf("%d Iterations: After after 1: %ld\n", iterations, v2);
  printf("Answer %ld\n", v1 * v2);
  return 0;
}

