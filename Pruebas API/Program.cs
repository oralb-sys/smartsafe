using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;

class Program
{
    static void Main(string[] args)
    {
        string url = "https://daii.unsaac.edu.pe/smartsafe/api/eventos";

        string usuario = "23957778";
        string tipo = "Accidente";
        string descripcion = "Accidente vehicular registrado desde C#";
        string latitud = "-13.53195";
        string longitud = "-71.96746";

        // CAMBIA ESTA RUTA POR LA UBICACIÓN REAL DE TU FOTO
        string rutaFoto = @"C:\Users\Rinok\Desktop\paisaje.jpg";

        if (!File.Exists(rutaFoto))
        {
            Console.WriteLine("ERROR: No se encontró la imagen.");
            Console.WriteLine("Ruta: " + rutaFoto);
            Console.ReadKey();
            return;
        }

        Console.WriteLine("Enviando evento a SmartSafe...");
        Console.WriteLine();

        try
        {
            using (HttpClient cliente = new HttpClient())
            using (MultipartFormDataContent formulario =
                   new MultipartFormDataContent())
            {
                // Datos del formulario
                formulario.Add(
                    new StringContent(usuario),
                    "usuario"
                );

                formulario.Add(
                    new StringContent(tipo),
                    "tipo"
                );

                formulario.Add(
                    new StringContent(descripcion),
                    "descripcion"
                );

                formulario.Add(
                    new StringContent(latitud),
                    "latitud"
                );

                formulario.Add(
                    new StringContent(longitud),
                    "longitud"
                );

                // Leer imagen
                byte[] imagenBytes = File.ReadAllBytes(rutaFoto);

                ByteArrayContent contenidoImagen =
                    new ByteArrayContent(imagenBytes);

                // Tipo MIME de la imagen
                contenidoImagen.Headers.ContentType =
                    new MediaTypeHeaderValue("image/jpeg");

                // Agregar imagen al formulario
                formulario.Add(
                    contenidoImagen,
                    "foto",
                    Path.GetFileName(rutaFoto)
                );

                // Enviar solicitud POST
                HttpResponseMessage respuesta =
                    cliente.PostAsync(url, formulario).Result;

                Console.WriteLine(
                    "Código HTTP: " +
                    (int)respuesta.StatusCode
                );

                Console.WriteLine();

                string contenidoRespuesta =
                    respuesta.Content.ReadAsStringAsync().Result;

                Console.WriteLine("Respuesta de SmartSafe:");
                Console.WriteLine(contenidoRespuesta);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("ERROR:");
            Console.WriteLine(ex.Message);
        }

        Console.WriteLine();
        Console.WriteLine("Presiona una tecla para terminar...");
        Console.ReadKey();
    }
}