 import java.net.Socket;
 import java.util.Scanner;
 import java.io.PrintStream;
 import java.io.FileOutputStream;
 import java.io.File;
 
 public class Client{
    public static void main(String args[]){
        try{
            String server = "localhost";
            int port = 5210;
            Socket client = new Socket(server,5210);
            System.out.println("已链接到服务器，地址：" + server + "，端口：" + port);
            Scanner scan = new Scanner(client.getInputStream());
            scan.useDelimiter("\n");
            PrintStream out = new PrintStream(client.getOutputStream());
            File file = new File("./cur_log_data/base_data.csv");
            if(!file.exists()){
                file.createNewFile();
            }
            PrintStream write = new PrintStream(new FileOutputStream(file));
            boolean flag =true;
            while(flag){
                Thread.sleep(60000);
                out.println("need_data");
                if(scan.hasNext()){
                    write.println(scan.next());
                    analyzeData();
                }
            }
            client.close();
        }catch(Exception e){
            e.printStackTrace();
        }
      }
      public static void analyzeData(){
            Runtime runtime = Runtime.getRuntime();
            Process p = runtime.exec("./process_test_data.py");
            p.waitfor();
            System.out.println("正在处理数据...");
            Runtime runtime = Runtime.getRuntime();
            Process p = runtime.exec("./test_PA.py");
            p.waitfor();
      }
 }
