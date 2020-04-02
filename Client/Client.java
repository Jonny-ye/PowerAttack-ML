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
            //设置连接的服务器
            String server = "localhost";
            int port = 5210;
            client = new Socket(server,5210);
            Scanner in = new Scanner(client.getInputStream());
            in.useDelimiter(";");
            PrintStream out = new PrintStream(client.getOutputStream());
            System.out.println("已连接服务器，地址：" + client.	getInetAddress() + "，端口：" + client.getPort() + "\n");
            
            //创建数据缓存文件
            File file = new File("./test_data/base_data.log");
            if(!file.getParentFile().exists()){
                file.getParentFile().mkdirs();
            }
            PrintStream writefile = new PrintStream(new FileOutputStream(file));
            
            //读取服务器日志行数
            int lines = 10;
            int cnt = 5;
            while(cnt > 0){
                timer(3*lines);          //定时器
                out.println(lines);     //发送指令
                if(in.hasNext()){
//                     System.out.println(in.next());
                    writefile.println(in.next());
                    if(processData(lines)){       //处理数据
                        analyzeData();      //分析数据
                    }else{
                        //数据处理失败，尝试清除缓存日志
                        writefile.close();
                        if(file.exists()){
                            file.delete();
                        }
                        file.createNewFile();
                        writefile = new PrintStream(new FileOutputStream(file));
                    }
                }else{
                    break;
                }
                cnt--;
            }
            //发送关闭连接指令
            out.println("exit");
            
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
    //处理数据
    public static boolean processData(int lines) throws Exception{
        String cmd = "./process_test_data.py " +String.valueOf(lines);
        
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor()!=0){
            System.out.println("数据处理失败");
            return false;
        }
        return true;
    }
    //机器学习模型分析数据
    public static boolean analyzeData() throws Exception{
        String cmd = "./test_PA.py";
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        BufferedReader bufread = new BufferedReader(new InputStreamReader(process.getInputStream()));
        if(process.waitFor()!=0){
            System.out.println("数据计算失败");
            return false;
        }
        StringBuffer buf = new StringBuffer();
        String line;            
        while((line = bufread.readLine())!= null){                
            buf.append(line).append("\n");
        }
        System.out.println(buf.toString());
        return true;
    }
    public static void timer(int s)throws Exception{
        while((s--) > 0){
            System.out.printf("等待服务器搜集日志信息:%2ds\r" ,s);
            Thread.sleep(1000);
        }
        System.out.println("\n");
    }
 }
