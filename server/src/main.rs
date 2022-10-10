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
			// todo
		})
	}
}