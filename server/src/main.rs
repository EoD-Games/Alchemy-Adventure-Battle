use ezoauth;
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::env;
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
	let mut addr = "127.0.0.1:".to_string();
	let port = env::args().nth(1).unwrap_or_else(|| "8080".to_string());
	addr.push_str(&port);
	let listener = TcpListener::bind(&addr).await?;
	println!("Listening on {addr}");
	loop {
		let (mut socket, _) = listener.accept().await?;
		tokio::spawn(async move {
			let config = ezoauth::OAuthConfig {
				auth_url: "https://discord.com/api/oauth2/authorize",
				token_url: "https://discord.com/api/oauth2/token",
				redirect_url: "http://localhost:8696",
				client_id: "964274065508556800",
				client_secret: &env::var("AAB_OAUTH_SECRET").unwrap(),
				scopes: vec!["identify"]
			};
			let (rx, auth_url) = ezoauth::authenticate(config, "localhost:8696").expect("Failed to authenticate");
			println!("Client should authenticate at {auth_url}");
			socket.write_all(auth_url.as_bytes()).await.expect("Failed to send OAuth URL");
			// todo
		});
	}
}