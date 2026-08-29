//https://raw.githubusercontent.com/aishikmukherjee/Linked-lists-in-C/refs/heads/main/Creating%20Singly%20Linked%20List.c


// Header Files.....
#include <stdio.h>
#include <stdlib.h>

// Defining the structure of the NODE of the Singly Linked List...
typedef struct NODE
{
    int data;                 // Data to store in the node
    struct NODE* next;       // Pointer to the next node
} node;

// Defining Functions.....
void display(node* ptr);                // Function to display the created linked list
node* createLinkedList(int n);          // Function to create the Linked list

// Display() function implementation...................
void display(node* ptr)
{
    printf("\nLinked List: ");
    while(ptr != NULL)
    {
        printf("%d -> ", ptr->data);  // Print the data of the current node
        ptr = ptr->next;               // Move to the next node
    }
    printf("NULL\n");                   // End of the linked list
}

// CreateLinkedList() function implementation.............
node* createLinkedList(int n)           // n = Number of nodes to create
{
    node* head = NULL;                  // Head pointer of the linked list
    node* temp = NULL;                  // Temporary pointer for creating nodes
    node* p = NULL;                     // Pointer to connect nodes

    for(int i = 0; i < n; i++)
    {
        temp = (node*)malloc(sizeof(node)); // Allocate memory for a new node
        if (temp == NULL)                // Check if memory allocation was successful
        {
            printf("Memory allocation failed!\n");
            exit(1);                    // Exit if memory allocation fails
        }

        printf("\nEnter Data: ");       // Prompt for user input
        scanf("%d", &temp->data);       // Read user input
        temp->next = NULL;              // Initialize next pointer of the new node

        if(head == NULL)
        {
            head = temp;                // First node becomes the head
        }
        else
        {
            p = head;
            while(p->next != NULL)      // Traverse to the last node
            {
                p = p->next;
            }
            p->next = temp;             // Link the new node at the end
        }
    }
    return head;                         // Return the head of the linked list
}

// The main function implementation..............
int main()
{
    node* HEAD = NULL;                   // Head pointer for the linked list
    HEAD = createLinkedList(10);         // Create a linked list with 10 nodes
    display(HEAD);                       // Display the linked list

    // Freeing memory for the linked list
    node* current = HEAD;                // Pointer for traversing the list
    node* next;                          // Pointer for keeping track of the next node
    while (current != NULL)              // Loop through the list
    {
        next = current->next;            // Store the next node
        free(current);                   // Free the current node
        current = next;                  // Move to the next node
    }

    printf("\nMemory is freed successfully.............!!!\n");
    return 0;                            // Successful termination of the program
}
