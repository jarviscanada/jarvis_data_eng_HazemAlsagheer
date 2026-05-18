package ca.jrvs.apps.grep;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepLambdaImp implements JavaGrepLambda{
  private final Logger logger = LoggerFactory.getLogger(JavaGrepImp.class);
  private String regex;
  private String rootPath;
  private String outFile;

  @Override
  public void process() throws IOException{
    List<String> matchLines;
    List<File> listOfFiles= this.listFiles(this.rootPath).collect(Collectors.toList());
    logger.info("Found {} files under {} ", listOfFiles.size(),this.rootPath);
    logger.info("Reading Files for matches");
    matchLines=listOfFiles.stream().flatMap(f->{
      try {
        List<String> lines = this.readLines(f).filter(this::containsPattern).collect(
            Collectors.toList());
        logger.info("{} matches found in {}",lines.size(), f.getName());
        return lines.stream();

      } catch (IOException e) {

        throw new UncheckedIOException(e);
      }
    }).collect(Collectors.toList());

    this.writeToFile(matchLines);
  }

  @Override
  public Stream<File> listFiles(String rootDir) {
    try {
      return Files.walk(Paths.get(rootDir)).filter(Files::isRegularFile).map(Path::toFile);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  @Override
  public Stream<String> readLines(File inputFile) throws IOException {
    List<String> result;

    try(BufferedReader reader= new BufferedReader(new FileReader(inputFile.getAbsolutePath()))) {
      result=reader.lines().collect(Collectors.toList());
    } catch (FileNotFoundException e) {
      logger.error("Input file not found: {}", inputFile.getPath(), e);
      throw new IllegalArgumentException(e);
    } catch (IOException e) {
      logger.error("Failed to read file: {}", inputFile.getPath(), e);
      throw e;
    }
    return result.stream();
  }

  @Override
  public boolean containsPattern(String line){
    return line.matches(this.regex);
  }

  @Override
  public void writeToFile(List<String> lines) throws IOException{
    try(BufferedWriter writer= new BufferedWriter(new FileWriter(this.outFile))){
      lines.forEach(e->{
        try {
          writer.write(e);
          writer.newLine();
        } catch (IOException ex) {
            logger.error("Failed to write to file: {}",this.outFile);
            throw new UncheckedIOException(ex);
        }
        });
      logger.info("Successful write to file: {}", this.outFile);

    }
    catch(IOException e){
      logger.error("Cannot write to file: {}", this.outFile, e);
      throw e;
    }

  }

  @Override
  public String getRootPath() {
    return this.rootPath;
  }

  @Override
  public void setRootPath(String rootPath) {
    this.rootPath = rootPath;
  }

  @Override
  public String getRegex() {
    return regex;
  }

  @Override
  public void setRegex(String regex) {
    this.regex = regex;
  }

  @Override
  public String getOutFile() {
    return outFile;
  }

  @Override
  public void setOutFile(String outFile) {
    this.outFile = outFile;
  }

  public static void main(String[] args) {
    if(args.length!=3){
      throw new IllegalArgumentException("USAGE: JavaGrep regex rootDir outFile");
    }
    JavaGrepLambdaImp grep = new JavaGrepLambdaImp();
    grep.setRegex(args[0]);
    grep.setRootPath(args[1]);
    grep.setOutFile(args[2]);
    try {
      grep.process();
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

}
