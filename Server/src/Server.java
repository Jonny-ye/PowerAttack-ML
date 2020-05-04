import java.net.Socket;
import java.net.ServerSocket;
import java.util.List;
import java.util.ArrayList;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.RandomAccessFile;

//客户端线程
class ClientThread implements Runnable{
    private Socket client;
    private int time_unit;
    public ClientThread(Socket client){
        this.client = client;
        this.time_unit = 3;
    }
    public void run(){
        try{
            System.out.println(Thread.currentThread() + "：客户端连接");
            Scanner in = new Scanner(this.client.getInputStream());
            in.useDelimiter("\n");
            PrintStream out = new PrintStream(this.client.getOutputStream());
            
            boolean flag = true;
            while(flag){
                if(in.hasNext()){
                    String data = in.next().trim();
                    if("exit".equalsIgnoreCase(data)){
                        break;
                    }else{
                        String location = "./src/data/base.tmp";  //日志文件位置
                        int line = Integer.valueOf(data)/this.time_unit;
                        if(line>=1 && line<=50){      //判断行数合法性 
                            List<String> list = this.readLastNLine(new File(location), line); 
                            String str = this.reverseLines(list);
                            out.println(str);
                            System.out.println(Thread.currentThread() + "：向客户端发送数据");
                        }
                    }//else
                }else{
                   break;
                }
            }
            this.client.shutdownInput();
            this.client.shutdownOutput();
            this.client.close();
            System.out.println(Thread.currentThread() + "：客户端断开连接");
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    //数据行反转拼接
    public  String reverseLines(List<String> list){
        StringBuffer buf = new StringBuffer();
        for(int i=list.size()-1; i>=0; i--){
            buf.append((String)list.get(i));
            buf.append("\n");
        }
        buf.append(";");
        return buf.toString();
    }
    
    //读取文件最后N行
    public  List<String> readLastNLine(File file, int numRead){
        List<String> result = new ArrayList<String>();
        try{
            RandomAccessFile fileRead = new RandomAccessFile(file, "r");
            long pos = fileRead.length() - 1;
            int count = 0;
            while (pos >= 0){
                pos--;
                fileRead.seek(pos);
                if (fileRead.readByte() == '\n'){
                    result.add(fileRead.readLine());
                    if (++count == numRead){
                        break;
                    }
                }
            }
            fileRead.close();
        }catch (IOException e){
            e.printStackTrace();
        }
        return result;
    }
}

public class Server{
    public static void main(String[] args){
        try{
            Runtime runtime = Runtime.getRuntime();
            runtime.exec("./src/log_service.sh &");
            ServerSocket server = new ServerSocket(5973);     //启用端口
            System.out.println("服务器监控服务启动，端口：" + server.getLocalPort() + "\n");
            
            //等待客户端连接
            boolean flag=true;
            while(flag){
                Socket client = server.accept();
                new Thread(new ClientThread(client)).start();
            }
            server.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
