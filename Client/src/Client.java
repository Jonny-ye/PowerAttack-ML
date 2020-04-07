import java.net.Socket;
import java.util.Scanner;
import java.io.PrintStream;
import java.io.FileOutputStream;
import java.io.File;
import java.io.IOException;
 
 public class Client{
    public static void main(String args[]){
        
        //参数
        String server_ip = "localhost";  //服务器ip地址
        int time_s = 30;   //采集时间间隔
        int cnt = 5;       //采集次数
            
        Socket client = null;
        try{
            //连接服务器b1
            client = new Socket(server_ip, 5973);
            Scanner in = new Scanner(client.getInputStream());
            in.useDelimiter(";");
            PrintStream out = new PrintStream(client.getOutputStream());
            System.out.println("监控客户端启动\n已连接服务器，IP地址：" + client.	getInetAddress() + "\n");
            
            //数据缓存文件
            File file = new File("./test_data/base.tmp");
            PrintStream writefile = new PrintStream(new FileOutputStream(file));
            
            //读取服务器日志行数b2
            int row = time_s/3;
            while( (cnt--) > 0 ){
                timer(time_s);          //定时器倒计时
                out.println(row);       //发送要读取的日志行数
                if(in.hasNext()){       //阻塞等待输入
                    writefile.println(in.next());  //输出到缓存文件
                    if(processData(row)){          //预处理数据
                        analyzeData();             //分析数据
                    }
                }else{
                    break;
                }
            }
            out.println("exit");      //发送关闭连接指令
            client.shutdownInput();
            client.shutdownOutput();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                client.close();
                System.out.println("服务器断开连接");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    
    //预处理数据
    public static boolean processData(int row) throws Exception{
        String cmd = "./process_test_data.py " + String.valueOf(row);
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据处理失败");
            return false;
        }
        return true;
    }
    
    //机器学习模型分析数据
    public static void analyzeData() throws Exception{
        String cmd = "./test_pa.py";
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据计算失败");
        }
        Scanner scan = new Scanner(process.getInputStream());
        scan.useDelimiter("\n");
        while(scan.hasNext()){
            System.out.println(scan.next());
        }
        scan.close();
    }
    
    //倒计时器
    public static void timer(int s)throws Exception{
        while((s--) > 0){
            System.out.printf("等待服务器搜集日志信息:%2ds\r", s);
            Thread.sleep(1000);
        }
        System.out.println("\n");
    }
 }
