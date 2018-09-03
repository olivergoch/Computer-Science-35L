Oliver Goch

I ran into several issues in multithreading this program.
The only function that could be parallelized is the main function.
I pulled out the pixel creating part of the main funciton and
put it in a function called threadFunction. In the main function I 
looped through pthread_create and passed in threadFunction as an argument.
After pulling out the majority of the main function, certain variables were
left out of threadFunction, namely nthreads and scene.
The other issue was printing the final values. As I parallelized along the
pixels, I created a float to hold the final value finalValues. When we 
print the finalValues we print along the width and the height, the 
conditions of the loop that created those values.

The function was sped up by increasing the number of threads, as can be 
seen in the make log. As the number of threads increased, so did the
speed of the function
