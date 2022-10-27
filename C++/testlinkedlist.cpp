#include <iostream>
#include "linkedlist.hpp"

using namespace std;

// This function prints contents of
// linked list starting from head
void printList(shared_ptr<Node<int>> node)
{
	while (node != NULL)
	{
		cout << " " << node->data;
		node = node->next;
	}
}

// Driver code
int main()
{

	// Start with the empty list
	shared_ptr<Node<int>> head = make_shared<Node<int>>();
    head = nullptr;
	
	// Insert 6. So linked list becomes 6->NULL
	append(&head, 6);
	
	// Insert 7 at the beginning.
	// So linked list becomes 7->6->NULL
 	push(&head, 7);
	
	// Insert 1 at the beginning.
	// So linked list becomes 1->7->6->NULL
	push(&head, 1);
	
	// Insert 4 at the end. So
	// linked list becomes 1->7->6->4->NULL
	append(&head, 4);
	
	// Insert 8, after 7. So linked
	// list becomes 1->7->8->6->4->NULL
	insertAfter(head->next, 8); 

    // Insert 5 after 6. So linked
	// list becomes 1->7->8->6->5->4->NULL
    auto pointer = head;
    // shift the pointer by two slots
    for (size_t i = 0; i < 2; ++i)
        pointer = pointer->next;
    insertAfter(pointer->next, 5);

    // Insert 3 after 1. So linked
	// list becomes 1->3->7->8->6->5->4->NULL
    insertAfter(head, 3);
	
	cout << "Created Linked list is: ";
	printList(head);
	
	return 0;
}
// This code is contributed by rathbhupendra, arkajyotibasak
