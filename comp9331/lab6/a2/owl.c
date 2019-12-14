#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "Graph.h"
#define MAX 99999
#define VISITED 1

void words_input(char *dict){//get the input
	char *c = (char*)malloc(1024 * sizeof(char));
	if (c == NULL) {
            fprintf(stderr, "c: out of memory\n");
            exit(1);
        }
	char space[] = " ";
	*dict = '\0';
	while (scanf("%s", c) != EOF){//scan each char
		strcat(dict, c);
		strcat(dict, space);	
	}
	free(c);
}

int get_size(char *temp){//get the number of words (vertex)  -> (may be have duplicates)
	int flag = 0, count  = 0;
	while (*temp != '\0'){
		if (*temp == ' ' || *temp == '\t' || *temp == '\n'){
			flag = 0;
			temp++;	
		}
		else if(flag == 0){//throught the whitespace before and after words to get the number of words
			count++;
			flag = 1;
			temp++;
		}
		else{
			temp++;
		}
	}
	return count;
}

int get_real_size(char **word, int size){//by comparing (strcmp) get the real number of vertex without duplicates
	int duplicate = 0;
	for (int i = 0; i < size-1; i++){
		if (!strcmp(*(word+i), *(word+i+1))){//compare before and after
			duplicate++;
		}
	}
	return (size - duplicate);
}

void split(char *dict, char *word[]){//split the input string into string array *e.g. "abc def" -> split() -> {"abc", "def"}
	char *p = " \t\n";//all whitespace
	int i = 0;
	char *token = NULL;
	token = strtok(dict, p);
	while (token != NULL) {
		word[i++] = token;
		token = strtok(NULL, p);		
	}
}

void remove_duplicate(char *word[], char **old_word, int old_size){//remove duplicate words in string array
	word[0] = old_word[0];
	int size = 1;
	for (int i = 1; i < old_size; i++){
		if (strcmp(*(word+size-1), *(old_word+i))){
			word[size++] = old_word[i];
		} 
	}
}

bool differByOne(char *a, char *b){//justify whether two string are in ordered word ladder requirements
	int size_a = strlen(a), size_b = strlen(b);
	if (abs(size_a - size_b) > 1){//more than one letter
		return false;
	}
	else if (size_a == size_b){//changing one letter
		int times = 0, i;
		for (i = 0; i < size_a; i++){
			if (*(a+i) != *(b+i)){
				times++;
			}
		}
		if (times > 1){
			return false;
		}
		return true;		
	}
	else {
		if (size_a < size_b){
			int temp = size_a;
			size_a = size_b;
			size_b = temp;
			char *t = a;
			a = b;
			b = t;
		}
		int i, j, flag = 0, differ = -1;//adding or removing one letter
		for (i = 0; i < size_a; i++){
			if (flag == 1){
				j = i - 1;				
			}
			else{
				j = i;
				if (j == size_a - 1){
					return true;
				}			
			}
			if (*(a+i) != *(b+j)){
				flag = 1;
				differ++;
			}			
		}
		if (differ > 0){
			return false;
		}
		return true;
	}	
}

void print_dict(char *word[], int size, int start){//print the dict -> 0 for dictionart; 1 for longest ladders when len is 1
	if (start == 1){
		for (int i = 0; i < size && i < 99; i++){//longest ladders less than 99
			printf("%2d: %s\n", i+start, *(word+i));
		}
	}
	else{
		for (int i = 0; i < size; i++){
			printf("%d: %s\n", i+start, *(word+i));
		}
	}
}

void Floyd(Vertex *n_graph, Vertex *cost, int size){//through Floyd-Warshall algorithm get the shrest path, but when weight is negative, it will be the longest path
	for (Vertex i = 0; i < size; i++){
		for (Vertex j = 0; j < size; j++){
			for (Vertex k = 0; k < size; k++){
				if (*(n_graph+i*size+k) + *(n_graph+k*size+j) < *(n_graph+i*size+j) && *(n_graph+i*size+k) != MAX && *(n_graph+k*size+j) != MAX){//core
					*(cost+i*size+j) = k;
					*(n_graph+i*size+j) = *(n_graph+i*size+k) + *(n_graph+k*size+j);
				}
			}	
		}
	}
}


int get_max(Vertex *graph, int size){// get the longest length
	int max = 0;
	for(Vertex i = 0; i < size; i++){
		for (Vertex j = 0; j < size; j++){
			if (*(graph+i*size+j) != MAX){
				if (abs(*(graph+i*size+j)) > max){
					max = abs(*(graph+i*size+j));
				}
			}
		}
	}
	return max;
}

int visit[MAX];//record whether visit or not
int count = 1, step = 0;
void dfs(Vertex current, Vertex start, int max, Vertex *graph, int size, int step, int len, char *word[]){//through recursion dfs print the longest path
	if (count > 99){//prints less than 100
		exit(0);
	}
	if (abs(*(graph+start*size+current)) == max && step == len){// the recursion exit (whether the current point is the end point through path graph)
		printf("%2d: " ,count++);
		for (Vertex i = 0; i < size; i++){
			if (i == current){
				printf("%s", *(word+i));
			}
			else if (visit[i] == 1){
				printf("%s -> ", *(word+i));
			}
		}
		putchar('\n');
		return;
	}
	visit[current] = VISITED;
	for (int i = 0; i < size; i++){
		if (*(graph+current*size+i) != MAX && visit[i] != VISITED){//MAX means no path
			step++;
			visit[i] = VISITED;
			//printf("i: %d  step: %d\n", i, step);
			dfs(i, start, max, graph, size, step, len, word);
			step--;
			visit[i] = 0;
		}
	}
	visit[current] = 0;	

}

void print_longest_ladder(int max, Vertex *graph, int size, char *word[]){//because the list of owls must also be in alphabetic order,find the end of longest from light to right, up to down
	int flag;
	for (int i = 0; i < size; i++){
		flag = 0;//each line only needs one point , which can find all end in that line
		for (int j = 0; j < size; j++){
			if (abs(*(graph+i*size+j)) == max && flag == 0){
				dfs(i, i, max, graph, size, step, max, word);
				flag = 1;
			}
		}
	}
}


int main(void){
	//Phase 1
	char *dict = (char*)malloc(MAX * sizeof(char));
	if (dict == NULL) {
            fprintf(stderr, "dict: out of memory\n");
            exit(1);
        }
	words_input(dict);//get input
	int size_duplicate = get_size(dict);
	char *word_duplicate[size_duplicate];
	split(dict, word_duplicate);
	int size = get_real_size(word_duplicate, size_duplicate);
	char *word[size];
	remove_duplicate(word, word_duplicate, size_duplicate);//get input without duplicate
	printf("Dictionary\n");
	print_dict(word, size, 0);

	//Phase 2
	printf("Ordered Word Ladder Graph\n");
	Vertex n_graph[size][size];//negative weight map to calculate the longest path
	Graph graph = newGraph(size);
	int num_path = 0;//path number
	for (Vertex i = 0; i < size; i++){
		for (Vertex j = 0; j < size; j++){
			if(differByOne(word[i], word[j]) && i < j){//whether have path between two words
				n_graph[i][j] = -1;//if have, assign anegative weight to the path
				num_path++;
			}
			else{
				n_graph[i][j] = MAX;//if not, assgin a unreachable number
			}
			if (differByOne(word[i], word[j]) && i != j){
				insertEdge(newEdge(i, j), graph);//insert edge			
			}

		}
	}
	showGraph(graph);
	freeGraph(graph);

	//phase 3
	Vertex cost[size][size];	
	for (Vertex i = 0; i < size; i++){//initialize cost array
		for (Vertex j = 0; j < size; j++){
			cost[i][j] = 0;
		}
	}

	Floyd(*n_graph, *cost, size);//Floyd-Warshall algorithm get the shrest path
	int max = get_max(*n_graph, size), max_len = max + 1;//get the max length
	//3 situations
	if (size == 0){//s1->no any vertexes
		printf("Longest ladder length: %d\n", max);
		printf("Longest ladders:\n");
	}
	else if (size != 0 && num_path == 0){//s2->no any pathes
		printf("Longest ladder length: %d\n", max_len);
		printf("Longest ladders:\n");
		print_dict(word, size, 1);
	}
	else{//s3->have longest path
		printf("Longest ladder length: %d\n", max_len);
		printf("Longest ladders:\n");
		print_longest_ladder(max, *n_graph, size, word);
	}
	free(dict);
	return 0;
}
