---
archive_policy: text-only
attachments:
- filename: web-computer-science-object-oriented.html
  kind: document
  media_type: text/html
  role: original
  sha256: sha256:1c2b4fc84758955984443360dd626e2b39a3bac161c2087fd3bea1baf242bcc7
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-22d3691da3ac
  position:
    end: 472
    start: 0
    type: TextPositionSelector
  quote_sha256: sha256:fa55949c7ded6fc009c140c867bf90ef4a3bca49ebd2d8cc15346d846e3d041e
  selector:
    exact: 'Classes, Objects, and Methods

      The object-oriented extension of Objective CAML is integrated with the functional
      and

      imperative kernels of the language, as well as with its type system. Indeed,
      this

      last point is unique to the language. Thus we have an object-oriented,

      statically typed language, with type inference. This extension allows

      definition of classes and instances, class inheritance (including multiple

      inheritance), parameterized classes, and abstract classes.'
    prefix: ''
    suffix: ' Class interfaces are

      generated '
    type: TextQuoteSelector
  selector_sha256: sha256:b70017bf7b6fcbfd9656c4a8c339338f70d538945552f6f6d908b61d2aaaf308
  snapshot_sha256: sha256:2e5d8f17114d0cb3852376730bcd4e41e706549536366ddcc0ea1500c830eea8
extractor: trafilatura/2.2.0
id: web-computer-science-object-oriented
media_type: text/html
origin: external
raw_ref:
  path: archive/raw/1c2b4fc84758955984443360dd626e2b39a3bac161c2087fd3bea1baf242bcc7.html
  sha256: sha256:1c2b4fc84758955984443360dd626e2b39a3bac161c2087fd3bea1baf242bcc7
read_status: retrieved
retrieval:
  acquisition: fetch
  resolved_url: https://caml.inria.fr/pub/docs/oreilly-book/html/book-ora140.html
  url: https://caml.inria.fr/pub/docs/oreilly-book/html/book-ora140.html
schema_version: source/v1
snapshot_sha256: sha256:2e5d8f17114d0cb3852376730bcd4e41e706549536366ddcc0ea1500c830eea8
source_type: doc
vault_id: public
---
Classes, Objects, and Methods
The object-oriented extension of Objective CAML is integrated with the functional and
imperative kernels of the language, as well as with its type system. Indeed, this
last point is unique to the language. Thus we have an object-oriented,
statically typed language, with type inference. This extension allows
definition of classes and instances, class inheritance (including multiple
inheritance), parameterized classes, and abstract classes. Class interfaces are
generated from their definition, but may be made more precise through a
signature, similarly to what is done for modules.
 Object-Oriented Terminology
We summarize below the main object-oriented programming terms.
- 
class:
-  a class describes the contents of the objects that belong to it:
 it describes an aggregate of data fields (called instance variables),
 and defines the operations (called methods).
- object:
-  an object is an element (or instance) of a class; objects have
 the behaviors of their class. The object is the actual
 component of programs, while the class specifies how instances are
 created and how they behave.
- method:
-  a method is an action which an object is able to perform. 
- sending a message
-  sending a message to an object means asking
 the object to execute or invoke one of its methods.
 Class Declaration
The simplest syntax for defining a class is as follows. We shall develop this
definition throughout this chapter.
 Syntax 
 
p1, ..., pn are the parameters for the constructor of the
class; they are omitted if the class has no parameters.
An instance variable is declared as follows:
 Syntax 
 
When a data field is declared mutable, its value may be modified.
Otherwise, the value is always the one that was computed when expr was evaluated during object creation.
Methods are declared as follows:
 Syntax 
 
method name p1 ...pn = expr
Other clauses than val and method can be used in a class
declaration: we shall introduce them as needed. 
 Our first class example.
We start with the unavoidable class point: 
- 
the data fields x and y contain the coordinates of the point,
- 
two methods provide access to the data fields (get_x and get_y),
- 
two displacement methods (moveto: absolute displacement) and (rmoveto: relative displacement),
- 
one method presents the data as a string (to_string), 
- 
one method computes the distance to the point from the origin (distance). 
# class point (x_init,y_init) =
   object
     val mutable x = x_init
     val mutable y = y_init
     method get_x = x
     method get_y = y
     method moveto (a,b) =  x <- a ; y <- b 
     method rmoveto (dx,dy) =  x <- x + dx ; y <- y + dy 
     method to_string () =  
         "( " ^ (string_of_int x) ^ ", " ^ (string_of_int y) ^")"
     method distance () = sqrt (float(x*x + y*y))
   end ;;
Note that some methods do not need parameters; this is the case for get_x
and get_y. We usually access instance variables with
parameterless methods.
After we declare the class point, the system prints the following text:
class point :
  int * int ->
  object
    val mutable x : int
    val mutable y : int
    method distance : unit -> float
    method get_x : int
    method get_y : int
    method moveto : int * int -> unit
    method rmoveto : int * int -> unit
    method to_string : unit -> string
  end
This text contains two pieces of information. First, the type for objects of the class;
this type will be abbreviated as point. The type of an object is the
list of names and types of methods in its class. In our
example, point is an abbreviation for:
  
  < distance : unit -> unit; get_x : int; get_y : int;
    moveto : int * int -> unit; rmoveto : int * int -> unit;
    to_string : unit -> unit >
Next, we have a constructor for instances of class point, whose type
is int*int  -> oint. The constructor allows us to construct
point objects (we´ll just say ``points'' to be brief) from the initial
values provided as arguments. In this case, we
construct a point from a pair of integers (meaning the initial
position). The constructor point is used with the
keyword new. 
It is possible to define class types:
# type simple_point = < get_x : int; get_y : int; to_string : unit -> unit > ;;
type simple_point = < get_x : int; get_y : int; to_string : unit -> unit >
 Note 
 
Type point does not repeat all the informations shown after a class
declaration. Instance variables are not shown in the type. Only
methods have access to these instance variables.
 Warning 
 
A class declaration is a type declaration. As a consequence, it
cannot contain a free type variable. 
We will come back to this point later when we deal with type constraints
(page ??) and parameterized classes
(page ??).
 A Graphical Notation for Classes
We adapt the UML notation for the syntax of Objective CAML types.
Classes are denoted by a rectangle with three parts:
- 
 the top part shows the name of the class, 
-  the middle part lists the attributes (data fields) of a class instance,
-  the bottom part shows the methods of an instance of the class. 
Figure 15.1 gives an example of the graphical representation
for the class caml.
Figure 15.1: Graphical representation of a class.
Type information for the fields and methods of a class may be added.
 Instance Creation
An object is a value of a class, called an instance of the class. 
Instances are created with the generic construction primitive new,
which takes the class and initialization values as arguments.
 Syntax 
 
new name expr1 ...exprn
The following example creates several instances of class point, from
various initial values.
# let p1 = new point (0,0);;
val p1 : point = <obj>
# let p2 = new point (3,4);;
val p2 : point = <obj>
# let coord = (3,0);;
val coord : int * int = 3, 0
# let p3 = new point coord;;
val p3 : point = <obj>
In Objective CAML, the constructor of a class is unique, but you may define your own
specific function make_point for point creation: 
# let make_point x = new point (x,x) ;;
val make_point : int -> point = <fun>
# make_point 1 ;;
- : point = <obj>
 Sending a Message
The notation # is used to send a message to an object.
2
 Syntax 
 
 obj1#name p1 ...pn
The message with method name ``name'' is sent to the object
obj. The arguments p1, ..., pn are as
expected by the method name. The method must be defined by the class of the
object, i.e. visible in the type. The types of arguments must conform to the types
of the formal parameters. The following example shows several queries performed on
objects from the class point.
# p1#get_x;;
- : int = 0
# p2#get_y;;
- : int = 4
# p1#to_string();;
- : string = "( 0, 0)"
# p2#to_string();;
- : string = "( 3, 4)"
# if (p1#distance()) = (p2#distance())
 then print_string ("That's just chance\n")
 else print_string ("We could bet on it\n");;    
We could bet on it
- : unit = ()
From the type point of view, objects of type point can be used
by polymorphic functions of Objective CAML, just as any other value in the language: 
# p1 = p1 ;;
- : bool = true
# p1 = p2;;
- : bool = false
# let l = p1::[];;
val l : point list = [<obj>]
# List.hd l;;
- : point = <obj>
 Warning 
 
Object equality is defined as physical equality.
We shall clarify this point when we study the subtyping relation (page ??).