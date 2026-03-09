
async function waitBackend(port, timeout = 15000) {

  const start = Date.now();

  while (Date.now() - start < timeout) {

    try {

      const res = await fetch(`http://127.0.0.1:${port}/health`);

      if (res.ok) {
        return true;
      }

    } catch (e) { }

    await new Promise(r => setTimeout(r, 500));

  }

  return false;

}

module.exports = waitBackend;