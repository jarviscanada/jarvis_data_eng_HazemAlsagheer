package ca.jrvs.apps.practice;

import static org.junit.jupiter.api.Assertions.*;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class LambdaStreamExcImpTest {
  private LambdaStreamExcImp lam;
  @BeforeEach
  void setup(){
    lam= new LambdaStreamExcImp();
  }

  @Test
  void createStrStream() {

    String[] arr=  {"a","b","c"};
    assertArrayEquals(arr,lam.createStrStream(arr).toArray());
  }

  @Test
  void toUpperCase() {
    String[] arr=  {"a","b","c"};
    for (int i=0;i<arr.length;i++){
      arr[i]=arr[i].toUpperCase();
    }
    assertArrayEquals(arr,lam.toUpperCase(arr).toArray());

  }

  @Test
  void filter() {
    String[] arr=  {"a","b","c"};
    String[] expected = {"a","c"};
    assertArrayEquals(expected, lam.filter(Stream.of(arr),"b").toArray());
  }

  @Test
  void createIntStream() {
    int[] arr= {1,2,3,4,5,6,7,8};
    assertArrayEquals(arr,lam.createIntStream(arr).toArray());
  }

  @Test
  void toList() {
    List<String> expected=  Arrays.asList("a","b","c");
    assertEquals(expected,lam.toList(expected.stream()) );
  }

  @Test
  void testToListInt() {
    List<Integer> expected= Arrays.asList(1,2,3,4,5);
    assertEquals(expected,lam.toList(IntStream.of(1,2,3,4,5)));
  }

  @Test
  void testCreateIntStreamRange() {
    int[] arr= {0,1,2,3,4,5,6};
    assertArrayEquals(arr, lam.createIntStream(0,7).toArray());
  }

  @Test
  void squareRootIntStream() {
    int[] arr= {0,1,2,3,4,5,6};
    double[] expected = new double[7];
    for (int i=0;i<arr.length;i++){
      expected[i]=Math.sqrt(arr[i]);
    }
    assertArrayEquals(expected,lam.squareRootIntStream(IntStream.of(arr)).toArray());
  }

  @Test
  void getOdd() {
    int[] arr= {0,1,2,3,4,5,6};
    int[] expected={1,3,5};
    assertArrayEquals(expected, lam.getOdd(IntStream.of(arr)).toArray());
  }

  @Test
  void getLambdaPrinter() {
    ByteArrayOutputStream outputStream=new ByteArrayOutputStream();
    PrintStream original =System.out;
    try{
      System.setOut(new PrintStream(outputStream));
      lam.getLambdaPrinter("start>", "<finish").accept("message");
      assertEquals("start>message<finish\n", outputStream.toString());

    }
    finally {
      System.setOut(original);
    }
  }

  @Test
  void printMessages() {
    ByteArrayOutputStream outputStream=new ByteArrayOutputStream();
    PrintStream original =System.out;
    String[] arr={"msg1", "msg2", "msg3"};

    try{
      System.setOut(new PrintStream(outputStream));
      lam.printMessages(arr,lam.getLambdaPrinter("start>", "<finish"));
      assertEquals("start>msg1<finish\nstart>msg2<finish\nstart>msg3<finish\n", outputStream.toString());

    }
    finally {
      System.setOut(original);
    }
  }

  @Test
  void printOdd() {
    ByteArrayOutputStream outputStream=new ByteArrayOutputStream();
    PrintStream original =System.out;
    int[] arr={1,2,3};

    try{
      System.setOut(new PrintStream(outputStream));
      lam.printOdd(IntStream.of(arr),lam.getLambdaPrinter("odd number:", "!"));
      assertEquals("odd number:1!\nodd number:3!\n", outputStream.toString());

    }
    finally {
      System.setOut(original);
    }
  }

  @Test
  void flatNestedInt() {
    List<List<Integer>> list=new ArrayList<List<Integer>>();
    list.add(Arrays.asList(1, 2));
    list.add(Arrays.asList(3,4,5));
    List<Integer> expected = Arrays.asList(1,4,9,16,25);
    assertEquals(expected, lam.flatNestedInt(list.stream()).collect(Collectors.toList()));

  }
  @Test
  void flatNestedInt2() {
    List<List<Integer>> list=new ArrayList<List<Integer>>();
    list.add(Arrays.asList(1, 2));
    list.add(Arrays.asList(3,4,5));
    List<Integer> expected = Arrays.asList(1,4,9,16,25);
    assertEquals(expected, lam.flatNestedInt2(list.stream()).collect(Collectors.toList()));

  }
}