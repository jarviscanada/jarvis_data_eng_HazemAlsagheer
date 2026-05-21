# Introduction
The Java Grep application is a command-line program designed to mimic the functionality of the Linux grep command by recursively searching files for lines matching a given regular expression pattern. The project was implemented in Java using two different approaches: a traditional imperative implementation using loops and recursion, and a functional implementation using Java Streams and lambda expressions. Maven was used for dependency management and packaging, JUnit was used for testing, and Docker was used to containerize the application for portability and easier deployment.

# Quick Start
To run the application:

1. Clone the repository from GitHub
2. Navigate to the project directory containing the packaged .jar file
3. Run the following command:
```
    java -jar grep-1.0-SNAPSHOT.jar regex_pattern rootDirectory outputFile
```
## Arguments
- ``` regex_pattern ```  
The regex pattern used to search file contents
- ``` rootDirectory ```  
The root directory where recursive file scanning begins
- ``` outputFile ```  
The file where all matched lines will be written
### Example
```
java -jar grep-1.0-SNAPSHOT.jar "ERROR" "./logs" "results.txt"
```

# Implementation
## Pseudocode
```
matchedLines = []
for file in listFilesRecursively(rootDir)
  for line in readLines(file)
      if containsPattern(line)
        matchedLines.add(line)
writeToFile(matchedLines)
```
## Performance Issue
One performance concern in this application is the recursive traversal of large directory structures combined with repeated file IO operations. In the imperative implementation, all matched lines are collected into memory before being written to the output file, which can increase memory usage for very large searches.

To address this, a second implementation using Java Streams and lambda expressions was developed. The Streams approach improves code readability and leverages lazy evaluation during data processing. For substantially larger datasets, the application could be further optimized using parallel streams, although this was unnecessary for the current project scale due to multithreading overhead.

# Test

The application was tested both manually and through automated unit testing.

### Manual Testing
- Created sample directory structures containing multiple text files.
- Tested various regex patterns and edge cases via the project main method.

### Automated Testing
JUnit test cases were written to validate:
- Recursive file traversal.
- File reading functionality.
- Regex matching behavior.
- Output file writing.
- Edge cases such as empty directories and invalid paths.

# Deployment
The application was packaged into an executable .jar file using Maven and containerized using Docker. The Docker image was then pushed to Docker Hub, allowing the application to run consistently across different environments without requiring local dependency installation.

### Example Docker execution:
```
docker run --rm grep-app "ERROR" /data output.txt
```
# Improvement
1. Add runtime benchmarking and memory profiling to compare the iterative and Streams-based implementations under different dataset sizes and workloads.
2. Support additional grep-style command options such as case-insensitive matching, or inverted matching to more closely mirror Linux grep functionality.
3. Improve scalability by streaming matched lines directly into the output file instead of storing all matches in memory before writing.

