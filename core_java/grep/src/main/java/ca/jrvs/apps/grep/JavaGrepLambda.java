package ca.jrvs.apps.grep;
import java.io.*;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;

public interface JavaGrepLambda {
  /**
   * Top level search workflow
   * @throws IOException
   */

  void process() throws IOException;

  /**
   * Traverse a given directory and return all files
   * @param rootDir input directory
   * @return stream of files under the rootDir
   */
  Stream<File> listFiles(String rootDir);

  /**
   * Read a file and return all the lines
   *
   * Explain FileReader, BufferedReader, and character encoding
   *
   * @param inputFile file to be read
   * @return lines
   * @throws IllegalArgumentException if a given inputFile is not a file
   * @throws IOException
   */
  Stream<String> readLines (File inputFile) throws IOException;


  /**
   * check if a line contains the regex pattern (passed by user)
   * @param line input string
   * @return true if there is a match
   */
  boolean containsPattern(String line);

  /**
   * Write Lines to a file
   *
   * Explore:FileOutputStream, OutputStreamWriter, and BufferedWriter
   *
   * @param lines matched line
   * @throws IOException if write failed
   */
  void writeToFile(List<String> lines) throws IOException;

  String getRootPath();

  void setRootPath(String rootPath);

  String getRegex();

  void setRegex(String regex);

  String getOutFile();

  void setOutFile(String outFile);
}
