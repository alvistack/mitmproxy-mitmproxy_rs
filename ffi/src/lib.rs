extern crate core;

use std::sync::RwLock;

use once_cell::sync::Lazy;
use pyo3::{exceptions::PyException, prelude::*};

mod server;
mod task;
mod tcp_stream;
mod util;

static LOGGER_INITIALIZED: Lazy<RwLock<bool>> = Lazy::new(|| RwLock::new(false));

fn init_logger() -> PyResult<()> {
    if *LOGGER_INITIALIZED.read().unwrap() {
        // logger already initialized
        Ok(())
    } else if pyo3_log::try_init().is_ok() {
        // logger successfully initialized
        *LOGGER_INITIALIZED.write().unwrap() = true;
        Ok(())
    } else {
        // logger was not initialized and could not be initialized
        Err(PyException::new_err(
            "Failed to initialize mitmproxy_rs logger.",
        ))
    }
}

#[pymodule]
pub fn mitmproxy_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    // set up the Rust logger to send messages to the Python logger
    init_logger()?;

    // set up tracing subscriber for introspection with tokio-console
    #[cfg(feature = "tracing")]
    console_subscriber::init();

    m.add_function(wrap_pyfunction!(server::start_server, m)?)?;
    m.add_class::<server::WireGuardServer>()?;
    m.add_function(wrap_pyfunction!(util::genkey, m)?)?;
    m.add_function(wrap_pyfunction!(util::pubkey, m)?)?;

    #[cfg(windows)]
    m.add_function(wrap_pyfunction!(
        server::start_windows_transparent_proxy,
        m
    )?)?;
    #[cfg(windows)]
    m.add_class::<server::WindowsProxy>()?;

    m.add_class::<tcp_stream::TcpStream>()?;

    Ok(())
}
