import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ChatController {
    private DatagramSocket dgramSocket;
    //private DatagramSocket origSocket;
    private ChatGUI gui;

    public ChatController(ChatGUI gui, int port) {
        this.gui=gui;

        try {
            dgramSocket = new DatagramSocket(port);
            dgramSocket.setReuseAddress(true);

        } catch (SocketException ex) {
            Logger.getLogger(ChatController.class.getName()).log(Level.SEVERE, null, ex);
        }

        UDPListener udpDPListener = new UDPListener();
        udpDPListener.start();
    }

    public void sendMsg(InetAddress dstIP , int destPort, String msg) throws IOException {
        byte[] buf=msg.getBytes();
        DatagramPacket p = new DatagramPacket(buf,buf.length,dstIP,destPort);
        dgramSocket.send(p);
    }

    class UDPListener extends Thread {
        public UDPListener() {
            super();
        }

        @Override
        public void run() {
            byte[] buf = new byte[1024];
            DatagramPacket p = new DatagramPacket(buf,buf.length);
            while(true){
                try {
                    
                    dgramSocket.receive(p);
                    String msg= new String(p.getData(),0,p.getLength());
                    
                    gui.showMessage(msg);
                    System.out.println(msg);

                } catch (IOException ex) {
                    Logger.getLogger(ChatController.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
    }
}
