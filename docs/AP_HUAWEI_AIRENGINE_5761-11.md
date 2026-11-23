# Ficha técnica · Huawei AirEngine 5761-11

AP de interior WiFi 6 (802.11ax), con dos radios 2×2 y antenas internas inteligentes. Es el equipo elegido para los pisos 3, 4 y 5 (21 por piso, 63 en total).

**Ficha técnica oficial (PDF):** [Huawei AirEngine 5761-11 Datasheet](https://e.huawei.com/my/documents/products/enterprise-network/51d9432033204ad39eea5833f73b076f)

## Especificaciones

| Característica | Valor |
|---|---|
| Estándar | 802.11a/b/g/n/ac/ac Wave 2/ax (WiFi 6) |
| Radios | 2: 2,4 GHz y 5 GHz |
| MIMO | 2×2:2 en 2,4 GHz y 2×2:2 en 5 GHz |
| Velocidad máxima | 1,775 Gbit/s (combinada) |
| Usuarios máximos | Hasta 1.024 (el número real depende del entorno) |
| Antenas | Internas inteligentes, doble banda |
| Ganancia 2,4 GHz | 4 dBi por cadena (pico) · **2 dBi combinada** |
| Ganancia 5 GHz | 5 dBi por cadena (pico) · **3 dBi combinada** |
| Potencia de transmisión | 24 dBm por cadena · **27 dBm combinada** por radio |
| Ajuste de potencia | −10 a 24 dBm por cadena |
| Bluetooth | BLE 5.2 (consola Bluetooth e IoT) |
| Puerto de red | 1 × GE RJ45 10/100/1000 con entrada PoE |
| Otros puertos | USB 2.0 tipo A (2,5 W o 5 W), entrada DC 12 V |
| Alimentación | PoE 802.3at/af o adaptador 12 V DC ±10 % |
| Consumo máximo | 15,3 W (sin USB) |
| Con PoE 802.3af | La potencia baja a 22 dBm por radio y el USB queda deshabilitado |
| Dimensiones | Ø 220 × 50 mm |
| Peso | 1,05 kg |
| Montaje | Cielo (placa de yeso, perfil T, varilla), muro o caja de conexiones |
| Temperatura de operación | −10 °C a +50 °C |
| Humedad | 5 % a 95 % sin condensación |
| MTBF | 124 años |
| Gestión | Modo Fit (controladora WAC), iMaster NCE-Campus (nube) o modo Fat (autónomo) |

## Cómo se usa en el site survey

| Valor en el modelo | Dato del equipo |
|---|---|
| Ganancia 3 dBi (5 GHz) y 2 dBi (2,4 GHz) | Ganancia combinada de la ficha |
| Potencia ajustable de 3 a 27 dBm | Tope de 27 dBm combinado por radio |
| Potencia de diseño 17 dBm (5 GHz) / 11 dBm (2,4 GHz) | Muy por debajo del máximo, para celdas chicas en alta densidad |
| PIRE 5 GHz = 17 + 3 = 20 dBm | Lo muestra la herramienta al elegir un AP |

## Por qué este AP

- WiFi 6 con OFDMA y MU-MIMO, pensado para salas de clase con muchos equipos al mismo tiempo.
- 15,3 W de consumo: el switch Cisco Catalyst 9200L 24P PoE+ (370 W) alimenta sus APs con holgura. Se usa PoE+ (802.3at) para no perder potencia de radio.
- Puerto de 1 Gbps, suficiente para un AP 2×2.
- Se integra con la plataforma de gestión Huawei que use la sede (controladora WAC en modo Fit o iMaster NCE-Campus).

## Fuentes

- [AirEngine 5761-11, página del producto (Huawei Enterprise)](https://e.huawei.com/my/products/wlan/indoor-access-points/airengine-5761-11)
- [WLAN Hardware Installation and Maintenance Guide, AirEngine 5761-11 (Huawei Support)](https://support.huawei.com/enterprise/en/doc/EDOC1100278610/18f959e1/airengine-5761-11)
