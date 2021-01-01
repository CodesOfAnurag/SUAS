import os

def file_detect(path) :
    files = os.listdir(path)                #listing all the files present at the given path
    path = [os.path.join(path , f) for f in files ]         #making array of paths of all the files at the location
    
    return max(path, key = os.path.getctime)                #obtaining and returning
                                                            #the max of the creation time of the files at the location
        
        
def main() :                        #main Function
    print(os.getcwd())              #printing current working directory
    print('next step')
    curdir = os.getcwd()
    print(file_detect(curdir))
                   
main()
