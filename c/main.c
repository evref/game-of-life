#include<stdio.h>
#include<time.h>
#include<string.h>

// Header
void game_of_life(int, int);


typedef struct
{
    int x, y;
} Cord;


int main()
{
    game_of_life(20, 10);
}


void clear_grid(int* grid, int length, int val)
{
    int i;
    for (i = 0; i < length; i++)
    {
        *(grid + i) = val;
    }
}
void print_grid(int* grid, int grid_width, int grid_height)
{
    int buffer_width = grid_width + 3;
    int buffer_height = grid_height;
    char buffer[buffer_width * buffer_height + 1];

    int i, j;
    for (j = 0; j < buffer_height; j++)
    {
        for (i = 0; i < buffer_width; i++)
        {
            int idx = (j * buffer_width + i);

            if (i == 0)
                *(buffer + idx) = '|';
            else if (i == buffer_width - 2)
                *(buffer + idx) = '|';
            else if (i == buffer_width - 1)
                *(buffer + idx) = '\n';
            else
            {
                int num_to_print = *(grid + (i - 1) + (j * (buffer_width - 3)));
                char char_to_print = '0';
                if (num_to_print != 0)
                    char_to_print = '1';

                *(buffer + idx) = char_to_print;
            }
            
        }
    }
    *(buffer + (buffer_width * buffer_height)) = '\n';

    printf("%s", buffer);
}

int count_neighbors(int* grid, int grid_width, int grid_height, Cord cord)
{
    int i, j, count = 0;
    for (j = cord.y - 1; j < cord.y + 2; j++)
    {
        for (i = cord.x - 1; i < cord.x + 2; i++)
        {
            // Check if out of bounds or if checking self
            if (i < 0 || j < 0 || i >= grid_width || j >= grid_height || i == cord.x && j == cord.y)
                continue;

            count += *(grid + (j * grid_width) + i);
        }
    }

    return count;
}
void next_state(int* grid, int grid_width, int grid_height)
{
    // Iterate through every cell and perform calculations
    int i, j;
    for (j = 0; j < grid_height; j++)
    {
        for (i = 0; i < grid_width; i++)
        {
            int idx = (j * grid_width) + i;
            int self_val = *(grid + idx);
            int neighbor_count = count_neighbors(grid, grid_width, grid_height, (Cord) {i, j});

            if (self_val == 1 && (neighbor_count < 2 || neighbor_count > 3))
                *(grid + idx) = 0;
            else if (self_val == 0 && neighbor_count == 3)
                *(grid + idx) = 1;
        }
    }
}

void game_of_life(int window_width, int window_height)
{
    int length = window_width * window_height;
    int grid[length];

    clear_grid(grid, length, 1);

    
    int i;
    for (i = 0; i < 10; i++)
    {
        print_grid(grid, window_width, window_height);
        next_state(grid, window_width, window_height);
    }
}