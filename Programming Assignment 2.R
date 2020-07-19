###################################Assignment Week 3###############################
#For this assignment we will be using the matlib library that has a function
#to get a matrix's inverse called inv(), first of all I focused on the vector
#examples that were given at the beginning of the assignment, I first changed 
#in the function makeVector the x, in the beginning it was numeric to create
#vectors, but I needed a matrix instead, after that, the code is basically
#the same as the vector, what changes is the inv() function that will give
#us the inverse of the matrix that we created, this functions focus on the article 
#Demistifying makeVector(), which was written by Len Greski´s, in here x is a 
#matrix and it is part of the function´s argument and m starts as a NULL values that
#will be used for further operations, then we use the operator <<- that is used 
#to assign the value on the right side to an object in the parent environment and
#avoids looking for the functions in the global environment and we then use the get function
#to get it from the parent environment, after this we define where we will set
#the inverse of the matrix and at the end an object is created by returning a list
#to the parent environment, after makeCacheMatrix is done, we have to create
#cacheSolve, another function that will retrieve information from makeCacheMatrix
#and will do the operation of the matrix´s inverse, here we will retrive information
#with the $ command and we put the condition if, and we want to know if the result is NULL
#if a matrix is set and if it is not NULL we have a valid cached inverse, otherwise if the result
#in !is.null(m) is false, we need to retrive the data from the matrix and get the inverse with
#the function inv(). In cacheSolve is where the inverse is executed, makeCacheMatrix is
#incomplete without cacheSolve, such as in teh example makeVector, both functions 
#complement each other to give us the result we need.


library(matlib)
makeCacheMatrix <- function(x = matrix()) {
  m <- NULL
  set <- function(y) {
    x <<- y
    m <<- NULL
  }
  get <- function() x
  setinverse <- function(inverse) m <<- inverse
  getinverse <- function() m
  list(set = set, get = get,
       setinverse = setinverse,
       getinverse = getinverse)
}

cacheSolve <- function(x, ...) {
  m <- x$getinverse()
  if(!is.null(m)) {
    message("getting cached data")
    return(m)
  }
  data <- x$get()
  m <- inv(data,...)
  x$setinverse(m)
  m
}

mat1 <- matrix(c(4,3,7,6,8,10,23,52,64), ncol = 3, nrow = 3)
t <- makeCacheMatrix(mat1)
cacheSolve(t)

#Results from previous example
#          [,1]        [,2]        [,3]
#[1,] -0.01990050 -0.38308458  0.31840796
#[2,]  0.42786070  0.23631841 -0.34577114
#[3,] -0.06467662  0.00497512  0.03482587