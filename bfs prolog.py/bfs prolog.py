%%%%%%% Best first search algorithm%%%%%%%%%
%%%
%%% This is one of the example programs from the textbook:
%%%
%%% Artificial Intelligence:
%%% Structures and strategies for complex problem solving
%%%
%%% by George F. Luger and William A. Stubblefield
%%%
%%% Corrections by Christopher E. Davis (chris2d@cs.unm.edu)
%%%
%%% These programs are copyrighted by Benjamin/Cummings Publishers.
%%%
%%% We offer them for use, free of charge, for educational purposes only.
%%%
%%% Disclaimer: These programs are provided with no warranty whatsoever as to
%%% their correctness, reliability, or any other property. We have written
%%% them for specific educational purposes, and have made no effort
%%% to produce commercial quality computer programs. Please do not expect
%%% more of them then we have intended.
%%%
%%% This code has been tested with SWI-Prolog (Multi-threaded, Version 5.2.13)
%%% and appears to function as intended.

%%%%% operations for state records %%%%%%%
%
% These predicates define state records as an adt
% A state is just a [State, Parent, G_value, H_value, F_value] tuple.
% Note that this predicate is both a generator and
% a destructor of records, depending on what is bound
% precedes is required by the priority queue algorithms
state_record(State, Parent, G, H, F, [State, Parent, G, H, F]).
precedes([,,,,F1], [,,,,F2]) :- F1 =< F2.

% go initializes Open and CLosed and calls path
go(Start, Goal) :-
empty_set(Closed),
empty_sort_queue(Empty_open),
heuristic(Start, Goal, H),
state_record(Start, nil, 0, H, H, First_record),
insert_sort_queue(First_record, Empty_open, Open),
path(Open,Closed, Goal).

% Path performs a best first search,
% maintaining Open as a priority queue, and Closed as
% a set.

% Open is empty; no solution found
path(Open,,) :-
empty_sort_queue(Open),
write("graph searched, no solution found").

% The next record is a goal
% Print out the list of visited states
path(Open, Closed, Goal) :-
remove_sort_queue(First_record, Open, _),
state_record(State, _, _, _, _, First_record),
State = Goal,
write('Solution path is: '), nl,
printsolution(First_record, Closed).

% The next record is not equal to the goal
% Generate its children, add to open and continue
% Note that bagof in AAIS prolog fails if its goal fails,
% I needed to use the or to make it return an empty list in this case
path(Open, Closed, Goal) :-
remove_sort_queue(First_record, Open, Rest_of_open),
(bagof(Child, moves(First_record, Open, Closed, Child, Goal), Children);Children = []),
insert_list(Children, Rest_of_open, New_open),
add_to_set(First_record, Closed, New_closed),
path(New_open, New_closed, Goal),!.

% moves generates all children of a state that are not already on
% open or closed.  The only wierd thing here is the construction
% of a state record, test, that has unbound variables in all positions
% except the state.  It is used to see if the next state matches
% something already on open or closed, irrespective of that states parent
% or other attributes
% Also, I've commented out unsafe since the way I've coded the water jugs
% problem I don't really need it.
moves(State_record, Open, Closed,Child, Goal) :-
state_record(State, _, G, ,, State_record),
mov(State, Next),
% not(unsafe(Next)),
state_record(Next, _, _, _, _, Test),
not(member_sort_queue(Test, Open)),
not(member_set(Test, Closed)),
G_new is G + 1,
heuristic(Next, Goal, H),
F is G_new + H,
state_record(Next, State, G_new, H, F, Child).

%insert_list inserts a list of states obtained from a  call to
% bagof and  inserts them in a priotrity queue, one at a time
insert_list([], L, L).
insert_list([State | Tail], L, New_L) :-
insert_sort_queue(State, L, L2),
insert_list(Tail, L2, New_L).

% Printsolution prints out the solution path by tracing
% back through the states on closed using parent links.
printsolution(Next_record, _):-
state_record(State, nil, _, ,, Next_record),
write(State), nl.
printsolution(Next_record, Closed) :-
state_record(State, Parent, _, ,, Next_record),
state_record(Parent, _, _, _, _, Parent_record),
member_set(Parent_record, Closed),
printsolution(Parent_record, Closed),
write(State), nl.

/*
printsolution(Next_record, Closed) :-
state_record(State, Parent, _, ,, Next_record),
state_record(Parent, Grand_parent, _, _, _, Parent_record),
member_set(Parent_record, Closed),
printsolution(Parent_record, Closed),
write(State), nl.
*/
