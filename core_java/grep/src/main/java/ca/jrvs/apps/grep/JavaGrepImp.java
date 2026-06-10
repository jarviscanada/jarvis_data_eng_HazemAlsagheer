package ca.jrvs.apps.grep;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JavaGrepImp implements JavaGrep {
  private final Logger logger = LoggerFactory.getLogger(JavaGrepImp.class);
  private String regex;
  private String rootPath;
  private String outFile;



  @Override
  public void process() throws IOException{
      List<String> matchLines = new ArrayList<>();
      List<File> listOfFiles= this.listFiles(this.rootPath);
      logger.info("Found {} files under {} ", listOfFiles.size(),this.rootPath);
      logger.info("Reading Files for matches");
      for (File f :listOfFiles){
        List<String> lines = this.readLines(f);
        int count=0;
        for (String l : lines){
          if (this.containsPattern(l)){
            count++;
            matchLines.add(l);
          }
        }
        logger.info("{} matches found in {}",count, f.getName());
      }
      this.writeToFile(matchLines);
  }

  @Override
  public List<File> listFiles(String rootDir){
    List<File> result= new ArrayList<>();
    File file= new File(rootDir);
    if (!file.exists()){
      logger.warn("Path does not exist!: {}", rootDir);
      return result;
    }

    File[] arrFiles=file.listFiles();

    if(arrFiles==null){
      return result;
    }
    for(File f: arrFiles){
      if (f.isDirectory()){
        result.addAll(this.listFiles(f.getPath()));
      }
      else if(f.isFile()) {
        result.add(f);
      }
    }

    return result;
  }

  @Override
  public List<String> readLines(File inputFile) throws IOException {
    List<String> result=new ArrayList<>();

    try(BufferedReader reader= new BufferedReader(new FileReader(inputFile.getAbsolutePath()))) {

      String line;
      while(((line=reader.readLine())!=null)){
        result.add(line);
      }
    } catch (FileNotFoundException e) {
      logger.error("Input file not found: {}", inputFile.getPath(), e);
      throw new IllegalArgumentException(e);
    } catch (IOException e) {
      logger.error("Failed to read file: {}", inputFile.getPath(), e);
      throw e;
    }
    return result;
  }

  @Override
  public boolean containsPattern(String line){
      return line.matches(this.regex);
  }

  @Override
  public void writeToFile(List<String> lines) throws IOException{
    try(BufferedWriter writer= new BufferedWriter(new FileWriter(this.outFile))){

      for(String s: lines){
        writer.write(s);
        writer.newLine();
      }
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

  public static void main(String[] args) throws IOException {
    if(args.length!=3){
      throw new IllegalArgumentException("USAGE: JavaGrep regex rootDir outFile");
    }
    JavaGrep grep = new JavaGrepImp();
    grep.setRegex(args[0]);
    grep.setRootPath(args[1]);
    grep.setOutFile(args[2]);
    try {
      grep.process();
    }catch(IOException e){
      throw e;
    }
  }
}
