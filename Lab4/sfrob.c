#include <stdio.h>
#include <stdlib.h>

#define end EOF

char decode(const char c)
{
    /*the char is frobnicated by xoring it with 00101010, or 42. To reverse this we xor it with 42.
     This also allows us to deal with unfrobnicated text without storing it in memory*/
    return c^42;
}

int frobcmp(char const *a, char const *b)
{
    for(;; a++, b++)
    {
        /*Space is the end of a word, so if both have a space, they're equal, but if one has a space and the other doesn't it's longer and greater
         Otherwise just compare (unfrobnicated) letters*/
        if(*a == ' ' && *b == ' ')
            return 0;
        else if (*b == ' ' || (decode(*a) > decode(*b)))
            return 1;
        else if(*a == ' ' || (decode(*a) < decode(*b)))
            return -1;
    }
}

void readError()
{
    if(ferror(stdin))
    {
        fprintf(stderr, "Error reading file");
        exit(1);
    }
}

int cmpQsort(const void* a, const void* b)
{
    const char* left = *(const char**) a;
    const char* right = *(const char**) b;
    return frobcmp(left, right);
}


int main(void)
{
    /*Declare array(dynamic c string) and array of pointers to hold our input*/
    char* word;
    char** wordarray;
    /*Alloacte memory*/
    word = (char*)malloc(sizeof(char));
    wordarray = (char**)malloc(sizeof(char*));
    /*Declare variables to keep track of arrays*/
    int numLetters = 0;
    int numWords = 0;
    /*w    o r d
      ^    ^
     curr next
     We do this to keep track of when the end of file comes and if we need to account for spaces*/
    char curr = getchar();
    readError();
    char next = getchar();
    readError();
    /*Have to do this everytime we read in case of an error*/
    //char next = getchar();
    while(curr != end && !ferror(stdin))
    {
        /*Take in letter and add it to word*/
        word[numLetters] = curr;
        /*Allocate space for word as it grows*/
        char* temp = realloc(word, (numLetters+2)*sizeof(char));
        if(temp != NULL)
            word = temp;
        /*Allocation didn't work, report an error*/
        else
        {
            free(word);
            fprintf(stderr, "Malloc Error");
            exit(1);
        }
        
        if(curr == ' ')
        {
            /*Add finished word to wordarray*/
            wordarray[numWords] = word;
            /*Allocate space for next word and set new word to null before allocating
             space for next one*/
            char** anotherOne = realloc(wordarray, (numWords+2)*sizeof(char*));
            if(anotherOne != NULL)
            {
                wordarray = anotherOne;
                numWords++;
                word = NULL;
                word = (char*)malloc(sizeof(char));
                numLetters = -1;
            }
            /*Else there was an allocation error, report an error*/
            else
            {
                free(wordarray);
                fprintf(stderr, "Malloc Error");
                exit(1);
            }
        }
        /*if we've reached the end of the file, break*/
        if(next == end && curr == ' ')
        {
            break;
        }
        /*If there a lot of spaces, ignore them*/
        else if (curr == ' ' && next == ' ')
        {
            /*Keep getting the spaces until you reach something that isn't a space*/
            while(curr == ' ')
            {
                curr = getchar();
                readError();
            }
            next = getchar();
            readError();
            numLetters++;
            continue;
        }
        /*If you reach the end of file and there's no space, add one*/
        else if(next == end)
        {
            curr = ' ';
            numLetters++;
            continue;
        }
        /*Get the next character and increment letter counter*/
        curr = next;
        next = getchar();
        readError();
        numLetters++;
    }
    
    qsort(wordarray, numWords, sizeof(char*), cmpQsort);
    int i;
    int j;
    for(i = 0; i < numWords; i++)
    {
        for(j = 0; ;j++)
        {
            //EOF error checking
            if(putchar(wordarray[i][j]) == EOF)
            {
                fprintf(stderr, "Putchar Error");
                exit(1);
            }
            if(wordarray[i][j] == ' ')
                break;
        }
    }
    /*Free all taken memory by freeing each word, then the whole array of words*/
    for(i = 0; i < numWords; i++)
        free(wordarray[i]);
    free(wordarray);
    exit(0);
}
