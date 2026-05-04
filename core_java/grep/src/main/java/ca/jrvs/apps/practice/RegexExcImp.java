package ca.jrvs.apps.practice;

public class RegexExcImp implements RegexExc {
  @Override
  public boolean matchJpeg(String filename){

    return filename.toLowerCase().matches(".*\\.jpe?g$");
  }

  @Override
  public boolean matchIp(String ip){
    return ip.matches("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}");
  }

  @Override
  public boolean isEmptyLine(String line){
    return line.matches("\\s*");
  }

  public static void main(String[] args) {
    RegexExc reg=new RegexExcImp();
    System.out.println(reg.matchJpeg("file.jpEg"));
    String ip="11.2.111.12";
    System.out.println("Matching Ip Method Result:"+ reg.matchIp(ip));
    System.out.println("EmptyLine Check: " + reg.isEmptyLine("    "));
  }
}
