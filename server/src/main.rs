use ezoauth;
use reqwest;
use serde_json::Value;
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
				client_id: "1029317200424730680",
				client_secret: &env::var("AAB_OAUTH_SECRET").unwrap(),
				scopes: vec!["identify"]
			};
			let (rx, auth_url) = ezoauth::authenticate(config, "localhost:8696").expect("Failed to authenticate");
			println!("Client should authenticate at {auth_url}");
			socket.write_all(auth_url.as_bytes()).await.expect("Failed to send OAuth URL");
			let ores = rx.recv().unwrap().expect("No token");
			let token = ores.access_token();
			let res: Value = serde_json::from_str(&reqwest::Client::new().get("https://discord.com/api/users/@me")
				.header(reqwest::header::AUTHORIZATION, format!("Bearer {token}"))
				.send()
				.await.expect("Failed to get user")
				.text()
				.await.expect("Failed to get text")
			).expect("Failed to dejson");
			let uid = res["id"].as_str().unwrap();
			let tag = format!("{}#{}", res["username"].as_str().unwrap(), res["discriminator"].as_str().unwrap());
			println!("Client with id {uid} and username {tag} has joined.");
			// todo
		});
	}
}