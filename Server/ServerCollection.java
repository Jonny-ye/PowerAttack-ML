
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.io.RandomAccessFile;
import java.util.List;
import java.util.ArrayList;

//System.currenTimeMillis()
//读取文件
class JyFile{
    public static StringBuffer reverseLines(List<String> list){
        StringBuffer buf = new StringBuffer();
        for(int i=list.size()-1; i>=0; i--){
            buf.append((String)list.get(i));
            buf.append("\n");
        }
        buf.append(";");
        return buf;
    }
    public static List<String> readLastNLine(File file, int numRead){
        List<String> result = new ArrayList<String>();
        if (!file.exists() || file.isDirectory() || !file.canRead()){
            return result;
        }
        try{
            int count = 0;
            RandomAccessFile fileRead = new RandomAccessFile(file, "r");
            long length = fileRead.length();
            if (length == 0L){
                return result;
            }else{
                long pos = length - 1;
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
            }
            fileRead.close();
        }
        catch (IOException e){
            e.printStackTrace();
        }
        return result;
    }
}

//客户端线程
class ClientThread implements Runnable{
    private Socket client;
    public ClientThread(Socket client){
        this.client = client;
    }
    public void run(){
        try{
            System.out.println(Thread.currentThread() + "：客户端连接");
            Scanner in = new Scanner(this.client.getInputStream());
            in.useDelimiter("\n");
            PrintStream out = new PrintStream(this.client.getOutputStream());
            while(true){
                if(in.hasNext()){
                    String data = in.next().trim();
                       if("exit".equalsIgnoreCase(data)){
                        break;
                    }else{
                        String location = "./log_data/base_data.log";
                        int num = Integer.valueOf(data);
                        if(num>=10 && num<=50){
                            List<String> list = JyFile.readLastNLine(new File(location),num);
                            StringBuffer buf = JyFile.reverseLines(list);
                            out.println(buf.toString());
                            System.out.println(Thread.currentThread() + "：向客户端发送数据");
                        }
                    }
                }else{
                   break;
                }
            }
            this.client.shutdownInput();
            this.client.shutdownOutput();
        }catch(Exception e){
            e.printStackTrace();
        }finally{
            try {
                this.client.close();
                System.out.println(Thread.currentThread() + "：客户端断开连接");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}
public class ServerCollection{
    public static void main(String[] args){
        try{
            Runtime runtime = Runtime.getRuntime();
            Process p = runtime.exec("./log_service.sh &");
            System.out.println("日志服务启动...");
            ServerSocket server = new ServerSocket(5210);     //启用端口
            System.out.println("服务器客户端启动...");
            System.out.println("服务器地址：" + server.getInetAddress() + "，开放端口：" + server.getLocalPort() + "\n");
            
            //等待客户端连接
            boolean flag=true;
            while(flag){
                Socket client = server.accept();              //等待客户端连接
                new Thread(new ClientThread(client)).start();
            }
            server.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
} 
 
 
