// Figures extracted from the original PDF, keyed by chapter number.
// Each entry is inserted next to the first paragraph of the chapter text that
// matches `at` (substring, or exact paragraph when `eq` is true):
//   mode "before" -> the figure goes above that paragraph (the paragraph is its caption)
//   mode "after"  -> the figure goes below that paragraph (the paragraph introduces it)
window.FIGURES = {
  "02": [
    {at:"Ilustración 1 CATEGOR", mode:"before", src:"images/ilustracion1.png", cap:"Ilustración 1 · Categorías del \"medio\" de la Administración de Contingencia (Luthans)"},
    {at:"Ilustración 2", mode:"before", src:"images/ilustracion2.png", cap:"Ilustración 2 · Marco conceptual de la Administración de Contingencia"}
  ],
  "03": [
    {at:"Ilustración 3", mode:"before", src:"images/ilustracion3.png", cap:"Ilustración 3 · Sistema cultural externo"}
  ],
  "04": [
    {at:"Ilustración 4", mode:"before", src:"images/ilustracion4.png", cap:"Ilustración 4 · El gerente según Sallenave"},
    {at:"Estrategia vs estructura:", mode:"after", src:"images/ilustracion5.png", cap:"Ilustración 5 · Estrategia vs estructura"},
    {at:"Clasificación según tipo de liderazgo", mode:"after", src:"images/ilustracion6.png", cap:"Ilustración 6 · El Grid Gerencial"}
  ],
  "05": [
    {at:"Ilustración 7", mode:"before", src:"images/ilustracion7.png", cap:"Ilustración 7 · Papeles del gerente según H. Mintzberg"},
    {at:"Ilustración 8", mode:"before", src:"images/ilustracion8.png", cap:"Ilustración 8 · Habilidades del gerente y la pirámide organizacional"}
  ],
  "07": [
    {at:"Ilustracion 9", mode:"before", src:"images/ilustracion9.png", cap:"Ilustración 9 · El continuo autocrático-democrático"},
    {at:"Ilustración 10", mode:"before", src:"images/ilustracion10.png", cap:"Ilustración 10 · La teoría situacional (Hersey y Blanchard)"},
    {at:"Ilustración 11", mode:"before", src:"images/ilustracion11.png", cap:"Ilustración 11 · Teoría de la ruta-meta (House)"}
  ],
  "08": [
    {at:"Ilustración 12", mode:"before", src:"images/ilustracion12.png", cap:"Ilustración 12 · Motivación"},
    {at:"Ilustración 13", mode:"before", src:"images/ilustracion13.png", cap:"Ilustración 13 · Pirámide de Maslow"}
  ],
  "10": [
    {at:"Ejemplos de las relaciones asimétricas", mode:"before", src:"images/tipologia-influencia.png", cap:"Tipología de la influencia según Schermerhorn (campo del poder y de la autoridad)"},
    {at:"Organización Burocrática", eq:true, mode:"before", src:"images/poder-jerarquia.png", cap:"Relaciones entre el poder real y la jerarquía formal"}
  ],
  "11": [
    {at:"Ilustración 14", mode:"before", src:"images/ilustracion14.png", cap:"Ilustración 14 · Delegación y autoridad"}
  ],
  "13": [
    {at:"El vector marca una dirección", mode:"after", src:"images/ilustracion15.png", cap:"Ilustración 15 · Vector de la perversidad"}
  ],
  "14": [
    {at:"Ilustración 16", mode:"before", src:"images/ilustracion16.png", cap:"Ilustración 16 · Cultura y estrategia"},
    {at:"Ilustración 17", mode:"before", src:"images/ilustracion17.png", cap:"Ilustración 17 · El modelo de las 5 fuerzas de Porter"},
    {at:"Ilustración 18 Cadena", mode:"before", src:"images/ilustracion18.png", cap:"Ilustración 18 · Cadena de valor de Porter"},
    {at:"PARTICIPACION RELATIVA EN EL MERCADO", mode:"before", src:"images/ilustracion19-bcg.png", cap:"Ilustración 19 · Matriz BCG", small:true},
    {at:"AMBITO", eq:true, mode:"before", src:"images/ilustracion19-foda.png", cap:"Ilustración 19 · Matriz FODA"},
    {at:"Futuro simplemente claro", mode:"before", src:"images/tipos-incertidumbre.png", cap:"Los cuatro tipos de incertidumbre (técnica de escenarios)"},
    {at:"- - Importancia ++", mode:"before", src:"images/escenarios-importancia-incertidumbre.png", cap:"Ranking de importancia e incertidumbre: seguir la franja amarilla y sobre todo el cuadrante rojo", small:true},
    {at:"Estas cuatro estrategias están ilustradas", mode:"after", src:"images/matriz-producto-mercado.png", cap:"Estrategias de crecimiento: matriz producto / mercado"}
  ],
  "15": [
    {at:"Ilustración 20", mode:"before", src:"images/ilustracion20.png", cap:"Ilustración 20 · Categorías de la información"}
  ],
  "16": [
    {at:"Tiempo disponible para decidir ADMINISTRATIVA", mode:"before", src:"images/ilustracion21.png", cap:"Ilustración 21 · Tipología de las situaciones problemáticas y críticas (Hermann)"},
    {at:"ideograma chino", mode:"after", src:"images/ideograma-crisis.png", cap:"Ideograma chino de \"crisis\": peligro + oportunidad", small:true}
  ]
};
