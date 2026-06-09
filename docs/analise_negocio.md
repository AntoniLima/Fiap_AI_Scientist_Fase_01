Análise de Negócio — NPS Preditivo

Tech Challenge Fase 1 — FIAP AI Scientist
________________________________________

1. Entendimento do Negócio

Qual problema de negócio está sendo resolvido?

A empresa não consegue agir sobre a satisfação do cliente antes que o problema aconteça. O NPS só é coletado depois que a jornada de compra se encerra — quando qualquer falha operacional já causou seu efeito. O que se busca resolver é a incapacidade de antecipar insatisfação: transformar dados operacionais disponíveis durante a jornada em sinais de alerta, permitindo intervenção proativa antes que a experiência se deteriore.
________________________________________

Por que o NPS é importante para um e-commerce?

Em e-commerce, trocar de fornecedor é simples e a concorrência é abundante. O NPS mede o que determina a decisão de recompra: a disposição do cliente em voltar e em recomendar. Além disso, variações na satisfação costumam preceder variações no faturamento — o que torna o NPS um indicador estratégico não só para CRM, mas para o planejamento do negócio.
________________________________________

Quais áreas poderiam se beneficiar desses insights?

Logística: atraso na entrega é o fator operacional que mais se associa à insatisfação neste case. Identificar rotas, regiões e janelas de prazo com maior risco permite agir preventivamente — renegociar SLAs, reforçar capacidade ou alertar o cliente antes que a frustração se instale.

Atendimento ao cliente: múltiplos contatos com o atendimento sinalizam que o problema não foi resolvido na primeira interação. Com visibilidade sobre pedidos em risco, o atendimento pode priorizar casos antes que o cliente precise de um segundo contato — que é onde a experiência quebra.

Produto e precificação: entender se valor do pedido, desconto e parcelamento influenciam a satisfação permite calibrar a política comercial. Um desconto alto que não se traduz em NPS elevado, por exemplo, pode indicar que o problema está na entrega, não no preço.

CRM e marketing: com a base segmentada entre promotores, neutros e detratores, é possível personalizar a comunicação — ativar promotores como canais de indicação, recuperar detratores com ações direcionadas e evitar cross-sell com clientes em momento de atrito.
________________________________________

Como o NPS impacta recompra, boca a boca e market share?

Cliente satisfeito volta e recomenda; insatisfeito não volta e compartilha a experiência negativa. Em e-commerce, avaliações em plataformas como Reclame Aqui, Google e marketplaces são consultadas antes da decisão de compra e afetam diretamente a conversão de novos clientes. O impacto sobre market share é cumulativo: uma base grande de detratores corrói reputação, reduz aquisição orgânica e força maior investimento em mídia para compensar a perda — com efeitos que aparecem nos números com defasagem.
________________________________________

Quais indicadores de mercado complementariam essa análise?

A base cobre bem a dimensão logística e de atendimento, mas não distingue se um atraso é problema interno ou limitação regional da infraestrutura de entrega. Dados de SLA médio por transportadora e por região complementariam diretamente a variável delivery_delay_days, permitindo separar o que é falha operacional da empresa do que é restrição de mercado. A ausência de informações sobre categoria de produto e canal de aquisição limita a segmentação do cliente — benchmarks de NPS por categoria de e-commerce ajudariam a contextualizar se o resultado reflete um problema da empresa ou uma característica do segmento em que opera. Por fim, a base registra reclamações internas (complaints_count), mas não captura insatisfação expressa em canais públicos — o volume de reclamações no Reclame Aqui e em marketplaces representaria uma camada de detração que os dados internos não alcançam.
________________________________________



2. Definição da Target

Qual variável representa a satisfação do cliente?

A variável que representa a satisfação do cliente é o nps_score — nota de 0 a 10 coletada após a experiência de compra.
Conceitualmente, é o alvo do problema de negócio: é o que a empresa quer melhorar. Mas do ponto de vista de um modelo preditivo acionável, o nps_score não pode ser o target do modelo — e essa distinção é importante.
________________________________________

Por que ela foi escolhida?

Porque é a métrica que a empresa já usa para medir satisfação, classifica clientes em promotores (9–10), neutros (7–8) e detratores (0–6), e orienta diretamente decisões de CRM, retenção e operações.
O problema é que essa variável só existe depois que a jornada se encerrou — entrega feita, atendimento concluído, reclamações registradas. Usá-la como target de um modelo preditivo significa treinar com informações que só aparecem no fim, o que inviabiliza qualquer ação proativa.
Por isso, o target operacional do modelo deve ser um evento intermediário observável durante a jornada. Atraso na entrega e múltiplos contatos com o atendimento são os eventos que mais se associam à insatisfação — e ambos podem ser monitorados em tempo real, permitindo intervenção antes da pesquisa NPS ser aplicada. O nps_score permanece como a métrica de negócio que a empresa quer melhorar; o evento de risco é o que o modelo aprende a prever.
________________________________________

Em que momento da jornada essa informação é coletada?

Após o encerramento completo da jornada — quando o cliente já recebeu o pedido e, eventualmente, já interagiu com o atendimento. Nesse ponto, todos os eventos operacionais já ocorreram e não podem mais ser revertidos.
É exatamente essa limitação que justifica o modelo preditivo: estimar o risco de insatisfação antes da pesquisa, usando sinais que surgem durante a jornada — como o segundo contato com o atendimento ou a detecção de atraso acima do limiar crítico.
________________________________________

Existe algum risco de usar essa variável de forma inadequada?

Sim. Os principais são:

Data leakage: variáveis como csat_internal_score e complaints_count têm correlação muito alta com o NPS, mas podem ter sido calculadas a partir de informações que incluem o próprio NPS ou eventos posteriores à jornada. Incluí-las como input sem verificar a origem temporal infla artificialmente a performance e torna o modelo inútil na prática.

Viés de resposta: nem todos os clientes respondem à pesquisa. Clientes muito satisfeitos ou muito insatisfeitos tendem a responder mais, distorcendo a distribuição da base e enviesando o modelo.

Generalização indevida: um modelo treinado em um período específico pode não generalizar para outros contextos — sazonalidade, novas regiões, mudanças operacionais. O modelo precisa ser monitorado continuamente e retreinado periodicamente.

