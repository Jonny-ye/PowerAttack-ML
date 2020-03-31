

import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.List;


class ReadFile{
    public static List<String> readLastNLine(File file, long numRead){
        List<String> result = new ArrayList<String>();
        if (!file.exists() || file.isDirectory() || !file.canRead()){
            return null;
        }
        try{
            long count = 0;
            RandomAccessFile fileRead = new RandomAccessFile(file, "r");
            long length = fileRead.length();
            if (length == 0L){
                return result;
            }else{
                long pos = length - 1;
                while (pos > 0){
                    pos--;
                    fileRead.seek(pos);
                    if (fileRead.readByte() == '\n'){
                        String line = fileRead.readLine();
                        result.add(line);
                        count++;
                        if (count == numRead){
                            break;
                        }
                    }
                }
                if (pos == 0)
                {
                    fileRead.seek(0);
                    result.add(fileRead.readLine());
                }
            }
            fileRead.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
        return result;
    }
}

class MyThread implements Runnable{
    private Socket client;
    public MyThread(Socket client){
        this.client = client;
    }
    public void run(){
        try{
            Scanner in = new Scanner(this.client.getInputStream());
            in.useDelimiter("\n");
            PrintStream out = new PrintStream(this.client.getOutputStream());
            boolean flag = true;
            while(flag){
                if(in.hasNext()){
                    String data = in.next().trim();
                    if("exit".equalsIgnoreCase(data)){
                        flag = false;
                        out.println("断开链接");
                    }else if("need_data".equals(data)){
                        String location = "./log_data/base_data.log";
                        out.println(ReadFile.readLastNLine(new File(location),20L));
                    }
                }
            }
            this.client.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}
public class ServerCollection{
    public static void main(String[] args){
        try{
            Runtime runtime = Runtime.getRuntime();
            Process p = runtime.exec("./pa_log_service.sh 3 wlp3s0 &");
            System.out.println("启动日志采集子进程...");
            ServerSocket server = new ServerSocket(5210);     //启用端口
            System.out.println("服务器监控主进程启动...");
            boolean flag = true;
            while(flag){
                Socket client = server.accept();              //等待客户端链接
                new Thread(new MyThread(client)).start();
            }
            server.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
} 
 
 
