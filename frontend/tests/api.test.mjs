import test from "node:test";
import assert from "node:assert/strict";
import { api } from "../src/api.js";

test("1. GET thanh cong tra ve du lieu JSON", async () => {
  const mockData = [{ class_id: "WEB-01", remaining: 1 }];
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    status: 200,
    text: async () => JSON.stringify(mockData),
  });

  try {
    const data = await api("/sections");
    assert.deepEqual(data, mockData);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("2. AbortError duoc giu nguyen khi request bi huy", async () => {
  const originalFetch = globalThis.fetch;
  const abortError = new Error("The user aborted a request.");
  abortError.name = "AbortError";
  globalThis.fetch = async () => {
    throw abortError;
  };

  try {
    await assert.rejects(
      async () => {
        await api("/sections");
      },
      (err) => err.name === "AbortError"
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("3. Loi mang/CORS nem thong bao ro rang", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => {
    throw new TypeError("Failed to fetch");
  };

  try {
    await assert.rejects(
      async () => {
        await api("/sections");
      },
      (err) => err.message.includes("Không nhận được phản hồi API")
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("4. DELETE thanh cong status 204 tra ve null", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    status: 204,
  });

  try {
    const data = await api("/enrollments/22000004/WEB-01", { method: "DELETE" });
    assert.equal(data, null);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("5. Phan hoi khong phai JSON nem loi ro rang", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    status: 200,
    text: async () => "<html>502 Bad Gateway</html>",
  });

  try {
    await assert.rejects(
      async () => {
        await api("/courses");
      },
      (err) => err.message.includes("phản hồi không phải JSON")
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("6. HTTP loi voi detail dang chuoi", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: false,
    status: 409,
    text: async () => JSON.stringify({ detail: "Lop hoc phan da het cho" }),
  });

  try {
    await assert.rejects(
      async () => {
        await api("/enrollments", { method: "POST", body: {} });
      },
      (err) => err.status === 409 && err.message.includes("Lop hoc phan da het cho")
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("7. HTTP loi 422 voi detail la danh sach item.msg", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: false,
    status: 422,
    text: async () =>
      JSON.stringify({
        detail: [{ msg: "Field required" }, { msg: "Invalid format" }],
      }),
  });

  try {
    await assert.rejects(
      async () => {
        await api("/enrollments", { method: "POST" });
      },
      (err) => err.status === 422 && err.message.includes("Field required; Invalid format")
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("8. POST kem body duoc JSON.stringify va co Content-Type", async () => {
  const originalFetch = globalThis.fetch;
  let sentHeaders, sentBody, sentMethod;
  globalThis.fetch = async (url, options) => {
    sentMethod = options.method;
    sentHeaders = options.headers;
    sentBody = options.body;
    return {
      ok: true,
      status: 201,
      text: async () => JSON.stringify({ message: "Created" }),
    };
  };

  try {
    const payload = { student_id: "22000004", class_section_id: "WEB-01" };
    await api("/enrollments", { method: "POST", body: payload });
    assert.equal(sentMethod, "POST");
    assert.equal(sentHeaders["Content-Type"], "application/json");
    assert.equal(sentBody, JSON.stringify(payload));
  } finally {
    globalThis.fetch = originalFetch;
  }
});
