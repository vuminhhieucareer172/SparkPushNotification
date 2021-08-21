package yourway.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Api {

	public static void main(String[] args) {
		try {
			SpringApplication.run(Api.class, args);
		} catch(Exception e) {
			System.out.println(e.getMessage());
		}
	}
}
