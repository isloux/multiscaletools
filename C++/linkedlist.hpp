// A complete working C++ program to
// demonstrate all insertion methods
// on Linked List
// Adapted from https://www.geeksforgeeks.org/linked-list-set-2-inserting-a-node
#include <bits/stdc++.h>
#include <memory>
#include <typeinfo>

// A linked list node
template<typename T>
class Node
{
	public:
        T data;
        std::shared_ptr<Node<T>> next;
};

// Given a reference (pointer to pointer)
// to the head of a list and an int, inserts
// a new node on the front of the list.
template<typename T>
void push(std::shared_ptr<Node<T>>* head_ref, T new_data)
{
	// 1. allocate node
	std::shared_ptr<Node<T>> new_node = std::make_shared<Node<T>>();

	// 2. put in the data
	new_node->data = new_data;

	// 3. Make next of new node as head
	new_node->next = *head_ref;

	// 4. move the head to point
	// to the new node
	*head_ref = new_node;
}

// Given a node prev_node, insert a new
// node after the given prev_node
template<typename T>
void insertAfter(std::shared_ptr<Node<T>> prev_node, T new_data)
{
	// 1. check if the given prev_node
	// is NULL
	if (prev_node == NULL)
	{
		std::cout << "The given previous node cannot be NULL\n";
		return;
	}

	// 2. allocate new node
	std::unique_ptr<Node<T>> new_node = std::make_unique<Node<T>>();

	// 3. put in the data
	new_node->data = new_data;

	// 4. Make next of new node
	// as next of prev_node
	new_node->next = prev_node->next;

	// 5. move the next of prev_node
	// as new_node
	prev_node->next = std::move(new_node);
}

// Given a reference (pointer to pointer)
// to the head of a list and an int,
// appends a new node at the end
template<typename T>
void append(std::shared_ptr<Node<T>>* head_ref, T new_data)
{

	// 1. allocate node
	std::unique_ptr<Node<T>> new_node = std::make_unique<Node<T>>();

	//used in step 5
	auto last = *head_ref;

	// 2. put in the data
	new_node->data = new_data;

	/* 3. This new node is going to be
	the last node, so make next of
	it as NULL*/
	new_node->next = NULL;

	/* 4. If the Linked List is empty,
	then make the new node as head */
	if (*head_ref == NULL)
	{
		*head_ref = std::move(new_node);
		return;
	}

	/* 5. Else traverse till the last node */
	while (last->next != NULL)
	{
		last = last->next;
	}

	/* 6. Change the next of last node */
	last->next = std::move(new_node);

	return;
}