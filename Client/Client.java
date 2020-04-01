 import java.net.Socket;
 import java.util.Scanner;
 import java.io.PrintStream;
 import java.io.FileOutputStream;
 import java.io.File;
 import java.io.InputStreamReader;
 import java.io.BufferedReader;
 import java.io.IOException;
 
 public class Client{
    public static void main(String args[]){
        Socket client = null;
        try{
            String server = "localhost";
            int port = 5210;
            client = new Socket(server,5210);
            System.out.println("已连接服务器，地址：" + server + "，端口：" + port + "\n");
            Scanner scan = new Scanner(client.getInputStream());
            scan.useDelimiter(";");
            PrintStream out = new PrintStream(client.getOutputStream());
            File file = new File("./test_data/base_data.log");
            if(!file.exists()){
                file.createNewFile();
            }
            PrintStream write = new PrintStream(new FileOutputStream(file));
            boolean flag =true;
            int cnt = 0;
            while(flag){
                out.println("need_data");
                if(scan.hasNext()){
                    timer(60); //倒计时60s
                    write.println(scan.next());
                    System.out.println("\n接收到第" + (++cnt) + "组数据...");
                    analyzeData();
                }
                if(cnt>=10){
                    out.println("exit");
                    break;
                }
            }
            client.shutdownInput();
            client.shutdownOutput();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                client.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
      }
      public static void analyzeData() throws Exception{
            Runtime runtime1 = Runtime.getRuntime();
            Process p1 = runtime1.exec("./process_test_data.py");
            p1.waitFor();
            System.out.println("通过机器学习模型计算数据...");
            Runtime runtime2 = Runtime.getRuntime();
            Process p2 = runtime2.exec("./test_PA.py");
            BufferedReader res = new BufferedReader(new InputStreamReader(p2.getInputStream()));
            p2.waitFor();
            String str = res.readLine();
            if("1".equals(str)){
                System.out.println("\n[警告] 当前服务器高负载，可能存在电力安全风险！\n");
            }else if("0".equals(str)){
                System.out.println("\n[安全] 服务器当前无潜在的电力攻击行为。\n");
            }else{
                System.out.println("返回暂无数据信息\n");
            }
        }
        public static void timer(int s)throws Exception{
            while((s--)> 0){
                System.out.printf("等待服务器搜集日志信息，倒计时：%2ds\r" ,s);
                Thread.sleep(1000);
            }
        }
 }
