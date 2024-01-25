#include <string>
#include "C:/Program Files/UraniumLang/io.h" 
#include "C:/Program Files/UraniumLang/random.h" 
int add ( int  a , int  b ) { 
    return a + b ;
} ;
int sub ( int  a , int  b ) { 
    return a - b ;
} ;
int main ( ) { 
    int num = add ( 10 , 5 ) ;
    uranium::io :: println ( "{}" , num ) ;
    return 0 ;
} ;
