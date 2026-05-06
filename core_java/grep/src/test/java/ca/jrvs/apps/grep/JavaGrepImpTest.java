package ca.jrvs.apps.grep;

import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.*;

class JavaGrepImpTest {

  private String rootDir;
  private String outFile;
  private JavaGrepImp grep;

  @BeforeEach
  public void setup(){
    this.rootDir = "./src/test/TestDir";
    this.outFile = "./src/test/TestOutput.txt";
    this.grep = new JavaGrepImp(".*=.*", rootDir, outFile);

  }

  @Test
  public void listFiles(){
    List<File> expected=new ArrayList<>();
    expected.add(new File("./src/test/TestDir/MixedTests.txt"));
    expected.add(new File("./src/test/TestDir/SubDir1/emptyFile.txt"));
    expected.add(new File("./src/test/TestDir/SubDir1/SpecialCharAndCaseSen.txt"));
    assertTrue(grep.listFiles(this.rootDir).containsAll(expected));
  }

  @Test
  public void containsPattern(){
    String sample1="+sasf==";
    String sample2="This sample has no equals and so should be false";

    assertTrue(grep.containsPattern(sample1));
    assertFalse(grep.containsPattern(sample2));
  }

  @Test
  public void readLines() throws IOException {
    List<String>lines= new ArrayList<>();
    lines.add("=");
    lines.add("==");
    lines.add("===");
    lines.add("");
    lines.add("");
    lines.add("key=value!");
    lines.add("key=value@");
    lines.add("key=value#");
    lines.add("");
    lines.add("");
    lines.add("Key=Value");
    lines.add("KEY=VALUE");
    lines.add("kEy=vAlUe");
    lines.add("");
    assertTrue(grep.readLines(new File("./src/test/TestDir/SubDir1/SpecialCharAndCaseSen.txt")).containsAll(lines));
  }
  @Test
  public void throwsIllegalArgumentException(){
    File missingFile = new File("src/test/TestDir/doesNotExist.txt");
    assertThrows(IllegalArgumentException.class, () -> { grep.readLines(missingFile); });

  }

  @Test
  public void writeToFiles() throws IOException {
    List <String> lines = new ArrayList<>();
    lines.add("line1");
    lines.add("line2");
    grep.writeToFile(lines);
    assertTrue(grep.readLines(new File(this.outFile)).containsAll(lines));
  }

  @Test
  public void throwsIOException(){
    String badPath = "nonexistent_dir/output.txt";
    JavaGrepImp grepTest = new JavaGrepImp(".*", "src/test", badPath);
    List<String> lines = new ArrayList<>();
    lines.add("Line Should Not Be Written");
    assertThrows(IOException.class, () -> { grepTest.writeToFile(lines); });
  }

  @Test
  public void settersAndGetters(){
    grep.setRegex("");
    assertEquals("",grep.getRegex());
    grep.setRootPath("/test");
    assertEquals("/test",grep.getRootPath());
    grep.setOutFile("test.txt");
    assertEquals("test.txt",grep.getOutFile());
  }


}