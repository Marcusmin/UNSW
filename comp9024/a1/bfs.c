#include <stdio.h>
#include <stdlib.h>
#define MAX 255
#define SX 0
#define SY 0
#define EX 3
#define EY 0

int map[4][4] = {
	{1,1,0,0},
	{0,1,1,1},
	{1,1,0,1},
	{1,0,0,1}
};

int move[4][2] = {
	{1,0},
	{-1,0},
	{0,1},
	{0,-1}
};

typedef struct node{
	int data;
	int x;
	int y;
	struct node *pre;	
}n, *np;

typedef struct queue{
	n node[MAX];
	int tail;
	int head;
}q, *qp;

qp queue_init(np n){
	qp queue = (qp)malloc(sizeof(q));
	if (!queue){
		printf("malloc failed\n");
		exit(1);
	}
	queue->tail = 1;
	queue->head = 0;
	queue->node[0] = *n;
	return queue;
}

n node_init(int x, int y){
	n start;
	start.data = map[x][y];
	start.x = x;
	start.y = y;
	start.pre = NULL;
	return start;
}

int empty(qp q){
	return (q->tail == q->head);
}

int full(qp q){
	return (q->tail > 255);
}


void queue_in(qp q, n item){
	if (full(q)){
		printf("the queue is full\n");
	}
	else{
		q->node[q->tail] = item;
		if (q->tail == 0){
			item.pre = NULL;
		}
		else{
			item.pre = &(q->node[q->tail-1]);
			
		}
		q->tail++;
	}
}

n queue_out(qp q){
	if (!empty(q)){
		return (q->node[q->head++]);
	}
	printf("empty!!!!\n");
	

}



int main(void){
	n node = node_init(SX, SY);
	qp q = 	queue_init(&node);	
	while (!empty(q)){
		node = queue_out(q);
		printf("%d %d\n",node.x, node.y);
		if (node.x == EX && node.y == EY){
			printf("solved\n");
			return 0;
		}
		for (int i = 0; i <= 3; i++){
			int new_x = node.x + move[i][0];
			int new_y = node.y + move[i][1];
			if (new_x < 0 || new_x > 4 || new_y < 0 || new_y > 4 || map[new_x][new_y] != 1){
				continue;			
			}
			//printf("---------------------------\n");
			n new_node = node_init(new_x, new_y);
			queue_in(q, new_node);
			map[node.x][node.y] = 0;
		}
		
	}
	printf("unsolved\n");
	return 0;
}
