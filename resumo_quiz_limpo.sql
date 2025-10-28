-- Arquivo SQL limpo para Hostinger
-- Gerado automaticamente - SEM comandos do phpmyadmin
-- Data: 2025-10-16 11:44:33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- IMPORTANTE: Este arquivo NÃO contém comandos do phpmyadmin
-- Selecionando o banco de dados da Hostinger
--
USE `u775269467_questoes`;

--
-- Estrutura da tabela `alternativas`
--

DROP TABLE IF EXISTS `alternativas`;
CREATE TABLE `alternativas` (
  `id_alternativa` int(11) NOT NULL AUTO_INCREMENT,
  `id_questao` int(11) NOT NULL,
  `texto` text NOT NULL,
  `eh_correta` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_alternativa`),
  KEY `id_questao` (`id_questao`),
  CONSTRAINT `alternativas_ibfk_1` FOREIGN KEY (`id_questao`) REFERENCES `questoes` (`id_questao`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=605 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `alternativas`
--

INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('361', '92', 'Pinça superior (preensão com ponta de polegar e indicador).', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('362', '92', 'Transferência de objetos de uma mão para a outra.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('363', '92', 'Empilhar blocos de forma coordenada.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('364', '92', 'Segurar o próprio corpo na posição de cócoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('365', '94', '10 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('366', '94', '12 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('367', '94', '18 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('368', '94', '24 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('373', '97', 'Balbuciar (repetição de sons como \'ba-ba\' ou \'ma-ma\').', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('374', '97', 'Compreender o próprio nome.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('375', '97', 'Formular frases com duas palavras.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('376', '97', 'Responder a gestos como \'tchau\'.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('377', '99', 'A criança está com um atraso significativo no desenvolvimento motor, pois já deveria  estar engatinhando.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('378', '99', 'O terapeuta ocupacional deve intervir imediatamente para corrigir a forma de locomoção  da criança.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('379', '99', 'O arrastar é uma forma de locomoção típica, e a criança está explorando seu ambiente  de maneira esperada para a idade.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('380', '99', 'A criança tem uma fraqueza muscular no tronco, que a impede de adotar a posição de  engatinhar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('381', '100', '2-4 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('382', '100', '6-9 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('383', '100', '12-18 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('384', '100', '2-3 anos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('385', '101', 'Compreender e seguir instruções de dois passos (\'pegue o sapato e coloque na caixa\').', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('386', '101', 'Copiar um círculo ou uma cruz com um lápis.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('387', '101', 'Nomear pelo menos 10 cores.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('388', '101', 'Reconhecer e nomear todas as letras do alfabeto.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('389', '102', '4-6 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('390', '102', '9-12 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('391', '102', '18-24 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('392', '102', '3-4 anos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('393', '103', 'Andar de bicicleta com rodinhas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('394', '103', 'Pular em um pé só.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('395', '103', 'Pular com os dois pés juntos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('396', '103', 'Correr sem cair.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('397', '104', 'Preensão em pinça inferior (com a lateral do polegar e o dedo indicador).', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('398', '104', 'Preensão em pinça superior (com a ponta do polegar e o dedo indicador).', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('399', '104', 'Preensão radial-palmar (segurar o objeto com os dedos e a base do polegar).', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('400', '104', 'Preensão palmar reflexa (segurar o dedo do adulto ao ser estimulado).', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('401', '105', '6-9 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('402', '105', '12-18 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('403', '105', '18-24 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('404', '105', '3-4 anos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('405', '106', 'É um sinal de medo e de um possível atraso no desenvolvimento social da criança.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('406', '106', 'É um reflexo arcaico de sobrevivência que tende a desaparecer após os 12 meses de  idade.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('407', '106', 'Indica a incapacidade da criança de tomar decisões autônomas, precisando sempre da  aprovação do cuidador.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('408', '106', 'É um marco do desenvolvimento social e emocional, demonstrando que a criança está  formando vínculos e usando as emoções do cuidador como guia.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('409', '107', '2 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('410', '107', '4 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('411', '107', '6 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('412', '107', '8 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('413', '108', 'Brincar predominantemente exploratório (levar objetos à boca).', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('414', '108', 'Brincar de faz-de-conta complexo, com papéis definidos (médico e paciente).', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('415', '108', 'Brincar solitário, ignorando outras crianças.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('416', '108', 'Brincar em grupo, compartilhando e negociando papéis.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('417', '109', 'Reflexo de Moro.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('418', '109', 'Reflexo de preensão palmar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('419', '109', 'Reflexo de busca.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('420', '109', 'Nenhuma das alternativas, todos já deveriam ter desaparecido.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('421', '110', 'Engatinhar de forma coordenada.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('422', '110', 'Caminhar com ajuda, segurando-se em móveis.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('423', '110', 'Correr de forma independente.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('424', '110', 'Subir escadas sem apoio.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('425', '111', 'Vestir-se completamente, incluindo fechos e botões.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('426', '111', 'Amarrar os próprios cadarços.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('427', '111', 'Usar talheres para cortar alimentos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('428', '111', 'Escovar os dentes sem supervisão.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('429', '112', '12-18 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('430', '112', '2-3 anos.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('431', '112', '4-5 anos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('432', '112', '6-7 anos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('433', '113', '12 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('434', '113', '18 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('435', '113', '24 meses.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('436', '113', '36 meses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('437', '114', 'Apontar para objetos nomeados.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('438', '114', 'Compreender o significado de frases curtas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('439', '114', 'Seguir instruções simples de um passo (como \'dê-me o brinquedo\').', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('440', '114', 'Responder a gestos como \'tchau\' e \'não\'.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('441', '115', 'Amarrar os cadarços de forma independente.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('442', '115', 'Cortar alimentos macios com faca e garfo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('443', '115', 'Limpar a si mesma após ir ao banheiro, com supervisão mínima.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('444', '115', 'Escovar os dentes de forma totalmente autônoma.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('445', '116', 'Transtorno do déficit de atenção.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('446', '116', 'Transtorno do Espectro Autista.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('447', '116', 'Transtorno específico da linguagem.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('448', '116', 'Transtorno opositor desafiador.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('449', '117', 'Sintoma negativo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('450', '117', 'Padrão restrito e repetitivo de comportamento.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('451', '117', 'Reação de estresse agudo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('452', '117', 'Resposta psicótica.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('453', '118', 'Treino de habilidades sociais em situações estruturadas.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('454', '118', 'Exclusão das atividades coletivas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('455', '118', 'Punição diante de condutas inadequadas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('456', '118', 'Reforço apenas de habilidades acadêmicas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('457', '119', 'Treinar leitura labial.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('458', '119', 'Estratégias de modulação sensorial.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('459', '119', 'Estímulo exclusivo da motricidade fina.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('460', '119', 'Exposição contínua a sons altos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('461', '120', 'Transtorno da fala.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('462', '120', 'Surdez congênita.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('463', '120', 'Transtorno do Espectro Autista.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('464', '120', 'Transtorno de conduta.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('465', '121', 'Utilizar os interesses como recurso para ampliar habilidades sociais.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('466', '121', 'Restringir totalmente o acesso ao tema.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('467', '121', 'Evitar atividades coletivas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('468', '121', 'Direcionar apenas para atividades motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('469', '122', 'Ecolalia.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('470', '122', 'Mutismo seletivo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('471', '122', 'Déficit auditivo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('472', '122', 'Linguagem pragmática preservada.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('473', '123', 'Estimular a independência funcional e comunicação.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('474', '123', 'Focar exclusivamente no treino motor.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('475', '123', 'Evitar interação social.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('476', '123', 'Priorizar conteúdos escolares.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('477', '124', 'Restrição alimentar por seletividade sensorial.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('478', '124', 'Fobia alimentar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('479', '124', 'Transtorno alimentar restritivo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('480', '124', 'Conduta opositor-desafiadora.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('481', '125', 'Adaptações no ambiente e suporte à participação.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('482', '125', 'Exclusão das aulas coletivas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('483', '125', 'Reforço de comportamentos inadequados.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('484', '125', 'Apenas treino motor fino.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('485', '126', 'Uso de atividades significativas que promovam autorregulação.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('486', '126', 'Correção por punição.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('487', '126', 'Evitar estimulação sensorial.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('488', '126', 'Exclusão de brincadeiras estruturadas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('489', '127', 'Perfil de desenvolvimento desigual.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('490', '127', 'Déficit global cognitivo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('491', '127', 'Transtorno de linguagem isolado.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('492', '127', 'Síndrome psicótica.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('493', '128', 'Valorizar diferenças e promover participação social.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('494', '128', 'Buscar normalizar totalmente o comportamento.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('495', '128', 'Priorizar isolamento social.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('496', '128', 'Focar apenas no desempenho acadêmico.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('497', '129', 'Uso de jogos simbólicos mediados.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('498', '129', 'Exclusão de brincadeiras de faz de conta.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('499', '129', 'Treino exclusivo de escrita.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('500', '129', 'Afastamento das atividades coletivas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('501', '130', 'Apoiar adaptações no ambiente laboral e promover inclusão.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('502', '130', 'Evitar participação social.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('503', '130', 'Reforçar apenas habilidades motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('504', '130', 'Exigir que se adapte sem suporte.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('505', '131', 'Estimular comunicação, cognição e interação social.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('506', '131', 'Focar apenas em habilidades motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('507', '131', 'Postergar o contato escolar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('508', '131', 'Evitar participação em grupo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('509', '132', 'Desenvolver habilidades sociais e cognitivas.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('510', '132', 'Reforçar isolamento social.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('511', '132', 'Evitar interação com pares.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('512', '132', 'Restringir interesses.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('513', '133', 'Ecolalia.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('514', '133', 'Afasia.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('515', '133', 'Mutismo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('516', '133', 'Taquifemia.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('517', '134', 'Participação em atividades significativas e desempenho ocupacional.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('518', '134', 'Somente a inteligência da criança.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('519', '134', 'Apenas habilidades motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('520', '134', 'Exclusivamente dados genéticos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('521', '135', 'Utilizar recursos estruturados e apoio visual.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('522', '135', 'Retirar permanentemente a criança da atividade.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('523', '135', 'Evitar qualquer rotina estruturada.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('524', '135', 'Delegar somente ao professor.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('525', '136', 'Déficits motores e alterações de linguagem.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('526', '136', 'Dificuldades de atenção, impulsividade e hiperatividade.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('527', '136', 'Desorganização espacial e alterações sensoriais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('528', '136', 'Déficits intelectuais e regressão cognitiva.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('529', '137', 'A ausência de prejuízos no desempenho escolar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('530', '137', 'A necessidade de estratégias para favorecer autorregulação e  organização.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('531', '137', 'Que a criança não apresenta dificuldades de socialização.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('532', '137', 'Que a criança não necessita de adaptações no ambiente.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('533', '138', 'Manifesta-se exclusivamente na adolescência.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('534', '138', 'Está sempre associado a deficiência intelectual.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('535', '138', 'Pode interferir no desempenho ocupacional em diferentes contextos.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('536', '138', 'É restrito ao ambiente escolar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('537', '139', 'Funções executivas.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('538', '139', 'Memória de longo prazo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('539', '139', 'Motricidade fina.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('540', '139', 'Compreensão semântica.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('541', '140', 'Estimular distrações durante atividades para maior flexibilidade.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('542', '140', 'Implementar rotinas estruturadas e apoio visual.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('543', '140', 'Evitar limites durante as tarefas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('544', '140', 'Utilizar somente atividades livres, sem regras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('545', '141', 'Persistência elevada em tarefas monótonas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('546', '141', 'Baixa tolerância à frustração e dificuldades em seguir regras.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('547', '141', 'Facilidade em manter foco seletivo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('548', '141', 'Desempenho superior em testes de atenção sustentada.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('549', '142', 'Baseia-se em exames laboratoriais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('550', '142', 'Depende de critérios clínicos e relatos de diferentes contextos.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('551', '142', 'É confirmado somente por neuroimagem.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('552', '142', 'Pode ser dado após único episódio de desatenção.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('553', '143', 'Treino de atividades exclusivamente motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('554', '143', 'Apoio às demandas acadêmicas e sociais, favorecendo autonomia.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('555', '143', 'Supressão de estímulos ambientais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('556', '143', 'Substituição da escola regular por ensino domiciliar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('557', '144', 'Estimular atividades com regras claras e feedback imediato.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('558', '144', 'Evitar rotinas e imprevisibilidade.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('559', '144', 'Permitir ausência de limites para favorecer criatividade.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('560', '144', 'Focar apenas em atividades individuais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('561', '145', 'Apenas habilidades motoras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('562', '145', 'O impacto do transtorno no desempenho ocupacional cotidiano.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('563', '145', 'Somente comportamentos em ambiente escolar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('564', '145', 'Exclusivamente habilidades de linguagem.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('565', '146', 'Atenção sustentada preservada em qualquer situação.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('566', '146', 'Dificuldade em inibir respostas impulsivas.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('567', '146', 'Ausência de prejuízos em habilidades sociais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('568', '146', 'Desenvolvimento intelectual abaixo da média em todos os casos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('569', '147', 'Devem envolver apenas a criança.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('570', '147', 'Podem incluir orientação familiar e adaptações ambientais.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('571', '147', 'Não devem considerar o contexto escolar.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('572', '147', 'São centradas somente no treino de força muscular.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('573', '148', 'Facilidade de planejamento de atividades.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('574', '148', 'Realização consistente de rotinas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('575', '148', 'Dificuldade em organizar materiais escolares.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('576', '148', 'Habilidade em concluir todas as tarefas sem apoio.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('577', '149', 'Apenas aspectos farmacológicos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('578', '149', 'Intervenções voltadas às ocupações significativas da criança.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('579', '149', 'Exclusivamente treino físico.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('580', '149', 'Atividades sem relação com a vida cotidiana.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('581', '150', 'Excesso de atenção a detalhes irrelevantes.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('582', '150', 'Facilidade em seguir instruções longas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('583', '150', 'Impulsividade em tomadas de decisão.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('584', '150', 'Lembrança precisa de tarefas adiadas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('585', '151', 'Atividades que alternem movimento e períodos de atenção dirigida.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('586', '151', 'Restrições físicas prolongadas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('587', '151', 'Exclusão de jogos de regras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('588', '151', 'Apenas atividades passivas de observação.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('589', '152', 'Não há associação com outros transtornos.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('590', '152', 'Podem estar presentes transtornos de aprendizagem e de conduta.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('591', '152', 'Está sempre vinculado ao autismo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('592', '152', 'Relaciona-se exclusivamente a epilepsia.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('593', '153', 'Estruturação do ambiente para reduzir distrações.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('594', '153', 'Eliminação de rotinas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('595', '153', 'Exclusão da criança de atividades em grupo.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('596', '153', 'Estímulo apenas em atividades digitais.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('597', '154', 'Tarefas longas e complexas, sem pausas.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('598', '154', 'Divisão de tarefas em etapas curtas com reforço positivo.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('599', '154', 'Evitar qualquer apoio visual.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('600', '154', 'Manter ambiente ruidoso e imprevisível.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('601', '155', 'Afeta apenas o desempenho motor.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('602', '155', 'Pode comprometer escola, relações sociais e atividades de vida  diária.', '1');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('603', '155', 'Manifesta-se exclusivamente em brincadeiras.', '0');
INSERT INTO `alternativas` (`id_alternativa`, `id_questao`, `texto`, `eh_correta`) VALUES ('604', '155', 'Restringe-se a dificuldades de fala.', '0');

--
-- Estrutura da tabela `assuntos`
--

DROP TABLE IF EXISTS `assuntos`;
CREATE TABLE `assuntos` (
  `id_assunto` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(150) NOT NULL,
  `descricao` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_assunto`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `assuntos`
--

INSERT INTO `assuntos` (`id_assunto`, `nome`, `descricao`, `created_at`) VALUES ('8', 'MARCOS DO DESENVOLVIMENTO INFANTIL', NULL, '2025-09-26 19:56:27');
INSERT INTO `assuntos` (`id_assunto`, `nome`, `descricao`, `created_at`) VALUES ('9', 'TRANSTORNO DO ESPECTRO AUTISTA (TEA)', NULL, '2025-09-26 20:12:15');
INSERT INTO `assuntos` (`id_assunto`, `nome`, `descricao`, `created_at`) VALUES ('11', 'TRANSTORNO DO DÉFICIT DE ATENÇÃO E HIPERATIVIDADE (TDAH)', NULL, '2025-10-14 10:36:48');

--
-- Estrutura da tabela `comentarios_questoes`
--

DROP TABLE IF EXISTS `comentarios_questoes`;
CREATE TABLE `comentarios_questoes` (
  `id_comentario` int(11) NOT NULL AUTO_INCREMENT,
  `id_questao` int(11) NOT NULL,
  `nome_usuario` varchar(100) NOT NULL,
  `email_usuario` varchar(100) DEFAULT NULL,
  `comentario` text NOT NULL,
  `data_comentario` timestamp NOT NULL DEFAULT current_timestamp(),
  `aprovado` tinyint(1) DEFAULT 1,
  `curtidas` int(11) DEFAULT 0,
  `id_comentario_pai` int(11) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT 1,
  `reportado` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_comentario`),
  KEY `idx_questao` (`id_questao`),
  KEY `idx_data` (`data_comentario`),
  KEY `idx_curtidas` (`curtidas`),
  KEY `idx_pai` (`id_comentario_pai`),
  KEY `idx_reportado` (`reportado`),
  CONSTRAINT `comentarios_questoes_ibfk_1` FOREIGN KEY (`id_questao`) REFERENCES `questoes` (`id_questao`) ON DELETE CASCADE,
  CONSTRAINT `comentarios_questoes_ibfk_2` FOREIGN KEY (`id_comentario_pai`) REFERENCES `comentarios_questoes` (`id_comentario`) ON DELETE CASCADE,
  CONSTRAINT `fk_comentario_pai` FOREIGN KEY (`id_comentario_pai`) REFERENCES `comentarios_questoes` (`id_comentario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `comentarios_questoes`
--

INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('2', '92', 'Bruno Collovini', 'bruno@teste.com', 'A-í= Hiato
De-pois= ditongo
car-re-ga-dor= RR é o dígrafo consonantal.', '2025-10-08 20:30:03', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('3', '92', 'Wandinha', 'wandinha@teste.com', 'LETRA A', '2025-10-08 20:30:03', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('4', '92', 'João Silva', 'joao@teste.com', 'Excelente questão! Ajudou muito no meu estudo.', '2025-10-08 20:30:03', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('5', '92', 'Usuário Teste Direto', 'teste@example.com', 'Este é um teste direto da API de comentários.', '2025-10-08 20:34:35', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('6', '94', 'Usuário Anônimo', '', 'oi teste teste teste', '2025-10-08 20:40:42', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('7', '94', 'Usuário Anônimo', '', 'teste teste teste', '2025-10-08 20:42:56', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('8', '99', 'Usuário Anônimo', '', 'kkkkkkkkkkkkkkkkkkkkk', '2025-10-08 20:49:07', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('9', '92', 'Usurio Annimo', '', 'teste teste teste', '2025-10-09 20:44:17', '1', '0', NULL, '0', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('10', '94', 'Usurio Annimo', '', 'teste teste teste', '2025-10-09 21:06:26', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('11', '94', 'Usurio Annimo', '', 'teste teste teste', '2025-10-09 21:11:45', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('12', '94', 'Usurio Annimo', '', 'teste que deu certo', '2025-10-09 21:12:03', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('13', '94', 'Usurio Annimo', '', 'kaique aqui', '2025-10-09 21:13:46', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('14', '94', 'Usuario Anonimo', '', 'mesmo ????', '2025-10-09 21:14:17', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('15', '100', 'Usurio Annimo', '', 'top mesmo em
kkk', '2025-10-10 12:17:38', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('16', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'top top toptop', '2025-10-10 17:16:31', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('17', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'top top  top', '2025-10-10 17:25:01', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('18', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'triste ..........', '2025-10-10 17:41:13', '1', '0', '17', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('19', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'top top top pp', '2025-10-10 18:13:49', '1', '0', '16', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('20', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'toptoptotptoto', '2025-10-10 18:18:24', '1', '0', '16', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('21', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'bobobobobobo', '2025-10-10 18:26:15', '1', '0', '17', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('22', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'toptoptoptop', '2025-10-10 18:26:48', '1', '0', '17', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('23', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'top  top oroototot', '2025-10-10 18:57:27', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('24', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'tototototototo', '2025-10-10 18:57:41', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('25', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'kfkfkgkgkgkg', '2025-10-10 18:57:45', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('26', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'fjfjfjfjfjfjfjfjfjf', '2025-10-10 18:57:51', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('27', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'toptotpotptotp', '2025-10-10 19:25:39', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('28', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'testetestetesteteste', '2025-10-10 19:45:45', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('29', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'testetstetse', '2025-10-10 19:46:27', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('30', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'ooooooooooooo', '2025-10-10 20:18:53', '1', '0', NULL, '0', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('31', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'testtestteste 1', '2025-10-10 20:22:08', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('32', '100', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'bom bombom', '2025-10-10 20:33:14', '1', '0', '31', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('33', '100', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'teste delete', '2025-10-10 21:07:38', '1', '0', '30', '0', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('34', '92', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'kkkkkkkkkkk', '2025-10-12 09:09:13', '1', '0', '9', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('41', '92', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'teste de comentario', '2025-10-12 17:17:30', '1', '0', NULL, '1', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('42', '92', 'Cleice Vitória Santana Cruz', 'cleicevitoria02@gmail.com', 'O bebê de 6 meses já demonstra um bom controle da linha média (levando objetos à boca com as duas mãos) e está desenvolvendo estabilidade no tronco (sentar com apoio).', '2025-10-12 20:47:16', '1', '0', NULL, '0', '1');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('43', '92', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'muito bom bom', '2025-10-13 20:45:55', '1', '0', '42', '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('44', '92', 'kaique lourran admin', 'kaiquenunis976@gmail.com', 'muito top em', '2025-10-13 21:57:34', '1', '0', NULL, '1', '0');
INSERT INTO `comentarios_questoes` (`id_comentario`, `id_questao`, `nome_usuario`, `email_usuario`, `comentario`, `data_comentario`, `aprovado`, `curtidas`, `id_comentario_pai`, `ativo`, `reportado`) VALUES ('45', '92', 'kaique lourran', 'hebertribeiro2222@gmail.com', 'top mesmo em', '2025-10-13 21:58:50', '1', '0', '44', '1', '0');

--
-- Estrutura da tabela `curtidas_comentarios`
--

DROP TABLE IF EXISTS `curtidas_comentarios`;
CREATE TABLE `curtidas_comentarios` (
  `id_curtida` int(11) NOT NULL AUTO_INCREMENT,
  `id_comentario` int(11) NOT NULL,
  `email_usuario` varchar(255) DEFAULT NULL,
  `ip_usuario` varchar(45) DEFAULT NULL,
  `data_curtida` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_curtida`),
  UNIQUE KEY `unique_curtida` (`id_comentario`,`ip_usuario`),
  UNIQUE KEY `unique_curtida_email` (`id_comentario`,`email_usuario`),
  UNIQUE KEY `unique_curtida_ip` (`id_comentario`,`ip_usuario`),
  KEY `idx_email_usuario` (`email_usuario`),
  KEY `idx_ip_usuario` (`ip_usuario`),
  CONSTRAINT `curtidas_comentarios_ibfk_1` FOREIGN KEY (`id_comentario`) REFERENCES `comentarios_questoes` (`id_comentario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `curtidas_comentarios`
--

INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('1', '2', NULL, '192.168.1.1', '2025-10-08 20:30:03');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('2', '2', NULL, '192.168.1.2', '2025-10-08 20:30:03');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('3', '2', NULL, '192.168.1.3', '2025-10-08 20:30:03');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('4', '2', NULL, '192.168.1.4', '2025-10-08 20:30:03');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('5', '3', NULL, '::1', '2025-10-08 20:33:55');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('6', '2', 'hebertribeiro2222@gmail.com', NULL, '2025-10-08 20:33:57');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('7', '13', NULL, '::1', '2025-10-09 21:14:07');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('11', '18', NULL, '::1', '2025-10-10 17:41:18');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('14', '15', NULL, '::1', '2025-10-10 18:33:18');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('19', '16', NULL, '::1', '2025-10-10 19:11:54');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('20', '17', NULL, '::1', '2025-10-10 19:11:56');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('21', '25', NULL, '::1', '2025-10-10 19:11:58');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('31', '27', NULL, '::1', '2025-10-10 19:45:25');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('47', '28', 'kaiquenunis976@gmail.com', NULL, '2025-10-10 20:10:49');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('59', '31', 'kaiquenunis976@gmail.com', NULL, '2025-10-10 20:33:55');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('61', '29', 'kaiquenunis976@gmail.com', NULL, '2025-10-10 20:43:39');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('62', '32', 'kaiquenunis976@gmail.com', NULL, '2025-10-10 20:43:50');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('63', '30', 'kaiquenunis976@gmail.com', NULL, '2025-10-10 21:07:14');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('64', '30', 'hebertribeiro2222@gmail.com', NULL, '2025-10-10 21:07:25');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('66', '9', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 09:08:53');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('67', '9', 'kaiquenunis976@gmail.com', NULL, '2025-10-12 09:09:06');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('69', '32', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 09:09:36');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('70', '34', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 09:10:02');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('87', '5', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 14:35:50');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('89', '5', 'kaiquenunis976@gmail.com', NULL, '2025-10-12 16:33:03');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('93', '26', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 16:49:52');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('94', '26', 'kaiquenunis976@gmail.com', NULL, '2025-10-12 16:50:05');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('96', '14', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 17:42:52');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('99', '14', 'kaiquenunis976@gmail.com', NULL, '2025-10-12 21:51:07');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('101', '8', 'kaiquenunis976@gmail.com', NULL, '2025-10-12 21:53:30');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('103', '41', 'hebertribeiro2222@gmail.com', NULL, '2025-10-12 21:59:30');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('104', '42', 'hebertribeiro2222@gmail.com', NULL, '2025-10-13 20:45:16');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('105', '42', 'kaiquenunis976@gmail.com', NULL, '2025-10-13 20:47:33');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('106', '43', 'kaiquenunis976@gmail.com', NULL, '2025-10-13 20:47:35');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('107', '41', 'kaiquenunis976@gmail.com', NULL, '2025-10-13 20:58:33');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('108', '44', 'kaiquenunis976@gmail.com', NULL, '2025-10-13 21:57:37');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('109', '44', 'hebertribeiro2222@gmail.com', NULL, '2025-10-13 21:58:26');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('110', '45', 'kaiquenunis976@gmail.com', NULL, '2025-10-13 21:59:10');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('111', '31', 'hebertribeiro2222@gmail.com', NULL, '2025-10-13 22:19:30');
INSERT INTO `curtidas_comentarios` (`id_curtida`, `id_comentario`, `email_usuario`, `ip_usuario`, `data_curtida`) VALUES ('112', '8', 'hebertribeiro2222@gmail.com', NULL, '2025-10-14 08:20:15');

--
-- Estrutura da tabela `denuncias_comentarios`
--

DROP TABLE IF EXISTS `denuncias_comentarios`;
CREATE TABLE `denuncias_comentarios` (
  `id_denuncia` int(11) NOT NULL AUTO_INCREMENT,
  `id_comentario` int(11) NOT NULL,
  `email_usuario` varchar(255) DEFAULT NULL,
  `ip_usuario` varchar(45) DEFAULT NULL,
  `motivo` text DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `data_denuncia` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_denuncia`),
  UNIQUE KEY `unique_denuncia_email` (`id_comentario`,`email_usuario`),
  UNIQUE KEY `unique_denuncia_ip` (`id_comentario`,`ip_usuario`),
  KEY `idx_denuncia_email` (`email_usuario`),
  KEY `idx_denuncia_ip` (`ip_usuario`),
  CONSTRAINT `denuncias_comentarios_ibfk_1` FOREIGN KEY (`id_comentario`) REFERENCES `comentarios_questoes` (`id_comentario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `denuncias_comentarios`
--

INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('1', '31', 'hebertribeiro2222@gmail.com', NULL, 'teste de tipo de relato', 'odio', '2025-10-12 17:02:47');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('2', '28', 'hebertribeiro2222@gmail.com', NULL, NULL, NULL, '2025-10-12 15:01:42');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('5', '14', 'kaiquenunis976@gmail.com', NULL, 'llllllllllll', 'outro', '2025-10-12 16:36:17');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('6', '26', 'hebertribeiro2222@gmail.com', NULL, 'kkkkkkkkkkkkk', 'assedio', '2025-10-12 16:49:44');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('9', '8', 'hebertribeiro2222@gmail.com', NULL, 'teste de violencia', 'violencia', '2025-10-12 17:10:12');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('10', '41', 'hebertribeiro2222@gmail.com', NULL, 'teste de tipo', 'violencia', '2025-10-12 17:17:48');
INSERT INTO `denuncias_comentarios` (`id_denuncia`, `id_comentario`, `email_usuario`, `ip_usuario`, `motivo`, `tipo`, `data_denuncia`) VALUES ('11', '42', 'hebertribeiro2222@gmail.com', NULL, 'mui assedio', 'assedio', '2025-10-13 20:45:34');

--
-- Estrutura da tabela `questoes`
--

DROP TABLE IF EXISTS `questoes`;
CREATE TABLE `questoes` (
  `id_questao` int(11) NOT NULL AUTO_INCREMENT,
  `id_assunto` int(11) NOT NULL,
  `enunciado` text NOT NULL,
  `explicacao` text DEFAULT NULL,
  `dificuldade` enum('fácil','médio','difícil') DEFAULT 'médio',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `alternativa_a` text DEFAULT NULL,
  `alternativa_b` text DEFAULT NULL,
  `alternativa_c` text DEFAULT NULL,
  `alternativa_d` text DEFAULT NULL,
  `alternativa_e` text DEFAULT NULL,
  `alternativa_correta` char(1) DEFAULT NULL,
  PRIMARY KEY (`id_questao`),
  KEY `id_assunto` (`id_assunto`),
  CONSTRAINT `questoes_ibfk_1` FOREIGN KEY (`id_assunto`) REFERENCES `assuntos` (`id_assunto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `questoes`
--

INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('92', '8', '(Fonte: adaptada de prova de residência em T.O.) Um bebê de 6 meses é capaz 
de sentar com apoio, rolar de bruços para as costas e levar objetos à boca com as duas 
mãos. De acordo com os marcos do desenvolvimento, qual habilidade motora fina seria a 
próxima a se desenvolver de forma típica?', '', 'médio', '2025-09-28 19:34:58', 'Alternativa A - Opção relacionada ao desenvolvimento motor fino', 'Alternativa B - Opção relacionada ao desenvolvimento cognitivo', 'Alternativa C - Opção relacionada ao desenvolvimento social', 'Alternativa D - Opção relacionada ao desenvolvimento emocional', 'Alternativa E - Opção relacionada ao desenvolvimento físico', 'A');
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('94', '8', '(Fonte: adaptada de prova de concurso para prefeitura) Com que idade é 
esperado que uma criança demonstre a capacidade de caminhar de forma autônoma, sem 
necessidade de apoio?', '', 'médio', '2025-09-28 19:37:07', 'Alternativa A - Opção relacionada ao desenvolvimento motor fino', 'Alternativa B - Opção relacionada ao desenvolvimento cognitivo', 'Alternativa C - Opção relacionada ao desenvolvimento social', 'Alternativa D - Opção relacionada ao desenvolvimento emocional', 'Alternativa E - Opção relacionada ao desenvolvimento físico', 'A');
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('97', '8', '(Fonte: adaptada de prova de residência multiprofissional) Em relação aos 
marcos da linguagem, qual das seguintes habilidades é a última a se desenvolver em uma 
sequência típica?', '', 'médio', '2025-09-28 19:54:43', 'Alternativa A - Opção relacionada ao desenvolvimento motor fino', 'Alternativa B - Opção relacionada ao desenvolvimento cognitivo', 'Alternativa C - Opção relacionada ao desenvolvimento social', 'Alternativa D - Opção relacionada ao desenvolvimento emocional', 'Alternativa E - Opção relacionada ao desenvolvimento físico', 'A');
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('99', '8', '(Fonte: adaptada de prova de concurso de T.O.) Um terapeuta ocupacional 
avalia uma criança de 9 meses. A mãe relata que o bebê prefere se arrastar no chão do que 
engatinhar. Qual das seguintes afirmações seria a mais apropriada para o profissional?', '', 'médio', '2025-09-28 19:58:37', 'Alternativa A - Opção relacionada ao desenvolvimento motor fino', 'Alternativa B - Opção relacionada ao desenvolvimento cognitivo', 'Alternativa C - Opção relacionada ao desenvolvimento social', 'Alternativa D - Opção relacionada ao desenvolvimento emocional', 'Alternativa E - Opção relacionada ao desenvolvimento físico', 'A');
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('100', '8', '(Fonte: adaptada de prova de residência em T.O.) Considerando os marcos do 
desenvolvimento social, com qual idade uma criança geralmente demonstra o medo de 
estranhos e a ansiedade de separação?', '', 'médio', '2025-09-28 19:59:21', 'Alternativa A - Opção relacionada ao desenvolvimento motor fino', 'Alternativa B - Opção relacionada ao desenvolvimento cognitivo', 'Alternativa C - Opção relacionada ao desenvolvimento social', 'Alternativa D - Opção relacionada ao desenvolvimento emocional', 'Alternativa E - Opção relacionada ao desenvolvimento físico', 'A');
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('101', '8', '(Fonte: adaptada de prova de concurso para T.O.) Um marco cognitivo 
importante para uma criança de 2 anos é a capacidade de:', '', 'médio', '2025-10-14 09:06:26', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('102', '8', '(Fonte: adaptada de prova de residência multiprofissional) O desenvolvimento do 
\'brincar funcional\' (usar objetos de acordo com sua função, como dirigir um carrinho) é um 
marco típico que surge em qual faixa etária?', '', 'médio', '2025-10-14 09:08:15', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('103', '8', '(Fonte: adaptada de prova de concurso para prefeitura) Qual das seguintes 
habilidades é a última a ser esperada no desenvolvimento da coordenação motora grossa 
de um pré-escolar (4-5 anos)?', '', 'médio', '2025-10-14 09:08:54', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('104', '8', '(Fonte: adaptada de prova de residência em T.O.) Um terapeuta ocupacional é 
solicitado a avaliar a preensão de um bebê de 7 meses. Qual tipo de preensão é a mais 
esperada para essa idade?', '', 'médio', '2025-10-14 09:09:33', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('105', '8', '(Fonte: adaptada de prova de concurso de T.O.) Em relação aos marcos da 
alimentação, com que idade é esperado que uma criança consiga beber de um copo aberto, 
com derramamento mínimo?', '', 'médio', '2025-10-14 09:10:15', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('106', '8', '(Fonte: adaptada de prova de residência multiprofissional) Um bebê de 10 
meses demonstra o \'olhar de referência social\', buscando a face do cuidador para verificar a 
reação dele antes de se aproximar de um objeto desconhecido. Qual das seguintes 
afirmações melhor descreve este comportamento?', '', 'médio', '2025-10-14 09:12:30', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('107', '8', '(Fonte: adaptada de prova de concurso de T.O.) Em qual idade um bebê é 
tipicamente capaz de rolar da posição de costas para a de bruços?', '', 'médio', '2025-10-14 09:13:22', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('108', '8', '(Fonte: adaptada de prova de residência em T.O.) Qual das seguintes 
características é esperada no brincar de uma criança de 3 anos?', '', 'médio', '2025-10-14 09:14:11', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('109', '8', '(Fonte: adaptada de prova de concurso para prefeitura) Um bebê de 4 meses 
demonstra qual dos seguintes reflexos primitivos que ainda não desapareceram?', '', 'médio', '2025-10-14 09:14:53', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('110', '8', '(Fonte: adaptada de prova de residência em T.O.) A capacidade de um 
terapeuta ocupacional é solicitada para um bebê de 12 meses. Qual é o marco motor 
esperado na locomoção dessa idade?', '', 'médio', '2025-10-14 09:16:10', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('111', '8', '(Fonte: adaptada de prova de concurso para T.O.) Qual das seguintes 
habilidades de autonomia é esperada de uma criança de 4 anos?', '', 'médio', '2025-10-14 09:16:53', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('112', '8', '(Fonte: adaptada de prova de residência multiprofissional) O \'brincar paralelo\', 
onde a criança brinca ao lado de outras crianças, mas sem interação direta, é típico de qual 
faixa etária?', '', 'médio', '2025-10-14 09:17:32', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('113', '8', '(Fonte: adaptada de prova de concurso de T.O.) A capacidade de construir uma 
torre de 6 blocos é um marco motor fino esperado para qual idade?', '', 'médio', '2025-10-14 09:18:26', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('114', '8', '(Fonte: adaptada de prova de residência em T.O.) Qual marco da linguagem 
receptiva é esperado de um bebê de 9 meses?', '', 'médio', '2025-10-14 09:19:02', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('115', '8', '(Fonte: adaptada de prova de residência em T.O.) Um terapeuta ocupacional 
avalia o desempenho de uma criança de 5 anos para atividades de vida diária. Qual das 
seguintes habilidades é a mais esperada para essa idade?', '', 'médio', '2025-10-14 09:19:56', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('116', '9', '(EBSERH – TO, 2019) Uma criança de 3 anos apresenta pouco contato 
visual, não responde ao ser chamada pelo nome e repete movimentos 
de balançar as mãos constantemente. A hipótese diagnóstica mais 
provável é:', '', 'médio', '2025-10-14 09:24:10', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('117', '9', '(Residência Multiprofissional – TO, UFRJ, 2021) Durante avaliação de 
uma criança com TEA, observa-se forte resistência a mudanças na 
rotina e crises quando um objeto é retirado. Este comportamento é 
caracterizado como:', '', 'médio', '2025-10-14 09:27:02', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('118', '9', '(EBSERH – TO, 2020) Na escola, um aluno com TEA tem dificuldades 
para compreender regras sociais simples, como esperar a vez de falar. 
O terapeuta ocupacional deve priorizar:', '', 'médio', '2025-10-14 09:30:01', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('119', '9', '(Residência TO – USP, 2023) Uma criança de 5 anos com TEA 
apresenta hipersensibilidade auditiva, cobrindo os ouvidos em 
ambientes ruidosos. A intervenção mais indicada é:', '', 'médio', '2025-10-14 09:30:43', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('120', '9', '(EBSERH – TO, 2018) Pais relatam que seu filho de 2 anos não 
balbucia, não aponta para objetos e não responde quando chamado 
pelo nome. O terapeuta deve considerar como hipótese principal:', '', 'médio', '2025-10-14 09:31:27', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('121', '9', '(Residência TO – UNIFESP, 2019) Uma adolescente com TEA 
apresenta interesses restritos em trens e recusa participar de atividades 
escolares fora desse tema. O papel do terapeuta ocupacional é:', '', 'médio', '2025-10-14 09:32:17', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('122', '9', '(EBSERH – TO, 2021) Durante a avaliação, nota-se que uma criança 
com TEA prefere brincar sozinha, repete falas de desenhos animados e 
apresenta dificuldade de comunicação funcional. Este comportamento é 
denominado:', '', 'médio', '2025-10-14 09:33:28', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('123', '9', '(Residência TO – UFMG, 2022) Uma criança com TEA de 4 anos 
apresenta atraso no desenvolvimento da linguagem e dificuldades em 
atividades de vida diária, como vestir-se. A prioridade inicial do TO será:', '', 'médio', '2025-10-14 09:34:20', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('124', '9', '(EBSERH – TO, 2020) Em um atendimento, a família relata que a 
criança com TEA só aceita comer alimentos de uma mesma cor. Esse 
comportamento está relacionado a:', '', 'médio', '2025-10-14 09:34:56', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('125', '9', '(Residência Multiprofissional – TO, UFBA, 2021) Na intervenção escolar 
de uma criança com TEA, o TO deve propor:', '', 'médio', '2025-10-14 09:35:57', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('126', '9', '(EBSERH – TO, 2022) Uma criança com TEA apresenta estereotipias 
motoras frequentes. A intervenção do TO deve considerar:', '', 'médio', '2025-10-14 09:36:41', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('127', '9', '(Residência TO – UNICAMP, 2023) Durante o atendimento, o TO 
observa que a criança com TEA consegue montar quebra-cabeças 
avançados para a idade, mas não estabelece contato visual. Isso 
exemplifica:', '', 'médio', '2025-10-14 09:38:07', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('128', '9', '(EBSERH – TO, 2017) Na perspectiva da neurodiversidade, a 
intervenção em TEA deve:', '', 'médio', '2025-10-14 09:40:33', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('129', '9', '(Residência TO – UERJ, 2019) Criança de 6 anos com TEA demonstra 
dificuldade em brincar simbolicamente. A estratégia terapêutica mais 
adequada é:', '', 'médio', '2025-10-14 09:41:15', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('130', '9', '(EBSERH – TO, 2019) No atendimento de um adulto com TEA que 
inicia estágio em empresa, o terapeuta deve:', '', 'médio', '2025-10-14 09:41:58', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('131', '9', '(Residência TO – USP, 2020) Em crianças pequenas com TEA, a 
intervenção precoce tem como objetivo:', '', 'médio', '2025-10-14 09:42:39', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('132', '9', '(EBSERH – TO, 2021) Uma criança com TEA apresenta hiperfoco em 
encaixar blocos de montar. O TO pode utilizar essa atividade para:', '', 'médio', '2025-10-14 09:43:39', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('133', '9', '(Residência Multiprofissional – TO, UNIFESP, 2022) Durante o brincar, 
uma criança com TEA repete frases sem sentido imediato. Esse 
fenômeno é chamado de:', '', 'médio', '2025-10-14 09:44:18', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('134', '9', '(EBSERH – TO, 2020) Na avaliação funcional de TEA, o TO deve 
investigar principalmente:', '', 'médio', '2025-10-14 09:45:29', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('135', '9', '(Residência TO – UFRJ, 2023) Uma criança com TEA tem dificuldades 
de autorregulação emocional, apresentando crises em ambientes novos. 
O TO deve:', '', 'médio', '2025-10-14 09:46:24', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('136', '11', '(EBSERH – 2022) Durante o atendimento a uma criança de 8 anos, os 
pais relatam dificuldade em manter a atenção em atividades escolares e 
esquecimentos frequentes, mesmo em tarefas simples. A terapeuta 
ocupacional suspeita de TDAH. Esse transtorno caracteriza-se 
principalmente por:', '', 'médio', '2025-10-14 10:38:13', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('137', '11', '(Residência Multiprofissional – HUPES/UFBA – 2021) No 
acompanhamento terapêutico ocupacional de crianças com TDAH, é 
fundamental considerar:', '', 'médio', '2025-10-14 10:39:04', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('138', '11', '(EBSERH – 2019) Em relação ao Transtorno de Déficit de Atenção e 
Hiperatividade, assinale a alternativa correta:', '', 'médio', '2025-10-14 10:39:43', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('139', '11', '(Residência TO – USP – 2020) Uma criança com TDAH apresenta 
dificuldades para planejar, iniciar e concluir atividades escolares. Essa 
dificuldade está relacionada a alterações em:', '', 'médio', '2025-10-14 10:40:17', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('140', '11', '(EBSERH – 2021) Entre as estratégias utilizadas pelo terapeuta 
ocupacional para crianças com TDAH, destacam-se:', '', 'médio', '2025-10-14 10:41:22', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('141', '11', '(Residência HUPE/UERJ – 2020) No contexto escolar, a criança com 
TDAH pode apresentar:', '', 'médio', '2025-10-14 10:42:06', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('142', '11', '(EBSERH – 2020) Sobre o diagnóstico do TDAH, é correto afirmar:', '', 'médio', '2025-10-14 10:43:08', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('143', '11', '(Residência – HC/UFMG – 2021) A intervenção terapêutica ocupacional 
com crianças com TDAH deve priorizar:', '', 'médio', '2025-10-14 10:44:01', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('144', '11', '(EBSERH – 2023) Em um grupo terapêutico de crianças com TDAH, o 
terapeuta ocupacional deve:', '', 'médio', '2025-10-14 10:44:42', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('145', '11', '(Residência UNIFESP – 2020) Na avaliação de crianças com TDAH, o 
terapeuta ocupacional deve atentar-se para:', '', 'médio', '2025-10-14 10:45:28', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('146', '11', '(EBSERH – 2018) Uma característica frequentemente observada no 
TDAH é:', '', 'médio', '2025-10-14 10:46:34', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('147', '11', '(Residência – HCFMRP/USP – 2019) Em relação às intervenções 
terapêuticas ocupacionais no TDAH:', '', 'médio', '2025-10-14 10:47:08', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('148', '11', '(EBSERH – 2022) Em crianças com TDAH, a desorganização 
ocupacional pode ser observada em:', '', 'médio', '2025-10-14 10:47:43', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('149', '11', '(Residência HU/UFS – 2021) Na perspectiva da Terapia Ocupacional, 
o trabalho com TDAH deve envolver:', '', 'médio', '2025-10-14 10:48:41', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('150', '11', '(EBSERH – 2017) Entre as manifestações comportamentais do 
TDAH, destaca-se:', '', 'médio', '2025-10-14 10:49:43', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('151', '11', '(Residência – HUOL/UFRN – 2020) Uma criança com TDAH apresenta 
dificuldade em permanecer sentada durante atividades escolares. O 
terapeuta ocupacional pode utilizar como estratégia:', '', 'médio', '2025-10-14 10:51:18', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('152', '11', '(EBSERH – 2021) Sobre as comorbidades do TDAH, é correto 
afirmar:', '', 'médio', '2025-10-14 10:52:35', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('153', '11', '(Residência – HC/UNICAMP – 2020) No manejo de crianças com 
TDAH, recomenda-se:', '', 'médio', '2025-10-14 10:53:05', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('154', '11', '(EBSERH – 2019) Uma criança de 7 anos, diagnosticada com TDAH, 
apresenta dificuldades em manter foco em atividades de escrita. A 
intervenção adequada inclui:', '', 'médio', '2025-10-14 10:53:38', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `questoes` (`id_questao`, `id_assunto`, `enunciado`, `explicacao`, `dificuldade`, `created_at`, `alternativa_a`, `alternativa_b`, `alternativa_c`, `alternativa_d`, `alternativa_e`, `alternativa_correta`) VALUES ('155', '11', '(Residência – HU/UFSC – 2021) Em relação ao impacto ocupacional 
do TDAH, pode-se afirmar:', '', 'médio', '2025-10-14 10:54:09', NULL, NULL, NULL, NULL, NULL, NULL);

--
-- Estrutura da tabela `relatorios_bugs`
--

DROP TABLE IF EXISTS `relatorios_bugs`;
CREATE TABLE `relatorios_bugs` (
  `id_relatorio` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `nome_usuario` varchar(255) NOT NULL,
  `email_usuario` varchar(255) NOT NULL,
  `tipo_problema` enum('bug','melhoria','duvida','outro') NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descricao` text NOT NULL,
  `pagina_erro` varchar(255) DEFAULT NULL,
  `status` enum('aberto','em_andamento','resolvido','fechado') DEFAULT 'aberto',
  `prioridade` enum('baixa','media','alta','critica') DEFAULT 'media',
  `resposta_admin` text DEFAULT NULL,
  `data_relatorio` timestamp NOT NULL DEFAULT current_timestamp(),
  `data_atualizacao` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_viu_resposta` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_relatorio`),
  KEY `idx_status` (`status`),
  KEY `idx_prioridade` (`prioridade`),
  KEY `idx_data` (`data_relatorio`),
  KEY `idx_usuario_viu` (`id_usuario`,`usuario_viu_resposta`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `relatorios_bugs`
--

INSERT INTO `relatorios_bugs` (`id_relatorio`, `id_usuario`, `nome_usuario`, `email_usuario`, `tipo_problema`, `titulo`, `descricao`, `pagina_erro`, `status`, `prioridade`, `resposta_admin`, `data_relatorio`, `data_atualizacao`, `usuario_viu_resposta`) VALUES ('1', '1', 'kaique lourran', 'kaiquenunis976@gmail.com', 'melhoria', 'melhorar sistema de acertos', 'estar muito ruim', 'index.php', 'resolvido', 'media', NULL, '2025-10-13 22:08:53', '2025-10-13 22:44:24', '0');
INSERT INTO `relatorios_bugs` (`id_relatorio`, `id_usuario`, `nome_usuario`, `email_usuario`, `tipo_problema`, `titulo`, `descricao`, `pagina_erro`, `status`, `prioridade`, `resposta_admin`, `data_relatorio`, `data_atualizacao`, `usuario_viu_resposta`) VALUES ('2', '1', 'kaique lourran', 'kaiquenunis976@gmail.com', 'bug', 'melhorar sistema de acertos', 'testes 2', 'quiz vertical', 'resolvido', 'media', 'obrigador , acabei de resolver', '2025-10-13 22:21:34', '2025-10-13 22:33:40', '1');
INSERT INTO `relatorios_bugs` (`id_relatorio`, `id_usuario`, `nome_usuario`, `email_usuario`, `tipo_problema`, `titulo`, `descricao`, `pagina_erro`, `status`, `prioridade`, `resposta_admin`, `data_relatorio`, `data_atualizacao`, `usuario_viu_resposta`) VALUES ('3', '1', 'Usuário Teste', 'teste@email.com', 'bug', 'Teste de Notificação', 'Esta é uma notificação de teste para verificar o sistema', NULL, 'resolvido', 'media', 'Sua solicitação foi resolvida com sucesso! Obrigado pelo feedback. Esta é uma resposta de teste do administrador.', '2025-10-13 22:29:11', '2025-10-13 22:32:42', '1');

--
-- Estrutura da tabela `respostas_usuario`
--

DROP TABLE IF EXISTS `respostas_usuario`;
CREATE TABLE `respostas_usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `id_questao` int(11) NOT NULL,
  `id_alternativa` int(11) NOT NULL,
  `acertou` tinyint(1) NOT NULL DEFAULT 0,
  `data_resposta` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_questao` (`id_questao`),
  KEY `idx_alternativa` (`id_alternativa`)
) ENGINE=InnoDB AUTO_INCREMENT=835 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dados da tabela `respostas_usuario`
--

INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('684', '2', '92', '364', '0', '2025-10-12 14:10:21');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('685', '2', '94', '365', '0', '2025-10-12 14:09:32');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('686', '2', '97', '375', '1', '2025-10-10 12:16:30');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('687', '2', '99', '379', '1', '2025-10-10 12:16:32');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('743', '1', '100', '384', '0', '2025-10-12 14:07:00');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('744', '1', '92', '362', '1', '2025-10-12 10:54:57');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('745', '1', '94', '367', '1', '2025-10-12 10:55:00');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('746', '1', '97', '375', '1', '2025-10-12 10:55:02');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('747', '1', '99', '379', '1', '2025-10-12 10:55:04');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('748', '2', '100', '383', '0', '2025-10-12 10:56:27');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('764', '2', '100', '384', '0', '2025-10-12 14:17:09');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('765', '2', '100', '382', '1', '2025-10-12 14:17:17');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('766', '2', '100', '381', '0', '2025-10-12 14:17:24');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('767', '2', '100', '381', '0', '2025-10-12 14:17:36');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('768', '2', '100', '384', '0', '2025-10-12 14:17:57');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('769', '2', '100', '382', '1', '2025-10-12 14:18:01');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('770', '2', '100', '382', '1', '2025-10-12 14:18:13');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('771', '2', '100', '383', '0', '2025-10-12 14:18:16');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('772', '2', '99', '380', '0', '2025-10-12 14:18:27');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('773', '2', '99', '380', '0', '2025-10-12 14:18:34');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('774', '2', '99', '380', '0', '2025-10-12 14:18:42');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('775', '2', '99', '379', '1', '2025-10-12 14:18:46');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('776', '2', '100', '384', '0', '2025-10-12 14:30:40');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('777', '2', '100', '384', '0', '2025-10-12 14:31:51');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('778', '2', '100', '381', '0', '2025-10-12 14:31:58');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('779', '2', '92', '361', '0', '2025-10-12 14:34:38');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('780', '2', '94', '367', '1', '2025-10-12 14:34:40');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('781', '2', '97', '376', '0', '2025-10-12 14:34:42');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('782', '2', '99', '379', '1', '2025-10-12 14:34:44');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('783', '2', '100', '382', '1', '2025-10-12 14:34:45');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('784', '1', '92', '362', '1', '2025-10-12 17:54:53');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('785', '1', '92', '362', '1', '2025-10-12 17:56:56');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('786', '3', '92', '362', '1', '2025-10-12 20:45:34');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('787', '3', '94', '367', '1', '2025-10-12 20:47:35');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('788', '3', '97', '375', '1', '2025-10-12 20:48:29');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('789', '3', '99', '380', '0', '2025-10-12 20:48:57');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('790', '3', '100', '382', '1', '2025-10-12 20:49:10');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('791', '2', '94', '365', '0', '2025-10-12 21:50:16');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('792', '3', '92', '362', '1', '2025-10-12 21:51:41');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('793', '3', '94', '367', '1', '2025-10-12 21:51:49');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('794', '3', '97', '375', '1', '2025-10-12 21:52:02');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('795', '1', '92', '363', '0', '2025-10-12 21:59:18');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('796', '1', '92', '362', '1', '2025-10-13 20:42:43');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('797', '1', '92', '363', '0', '2025-10-13 20:45:08');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('798', '2', '92', '364', '0', '2025-10-13 20:58:09');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('799', '2', '92', '361', '0', '2025-10-13 20:58:24');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('800', '2', '92', '361', '0', '2025-10-13 21:14:19');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('801', '2', '94', '368', '0', '2025-10-13 21:14:28');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('802', '2', '92', '362', '1', '2025-10-13 21:57:13');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('803', '2', '92', '361', '0', '2025-10-13 22:00:44');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('804', '2', '99', '377', '0', '2025-10-13 22:00:45');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('805', '2', '100', '381', '0', '2025-10-13 22:00:46');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('806', '1', '92', '362', '1', '2025-10-13 22:19:14');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('807', '1', '100', '382', '1', '2025-10-13 22:19:17');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('808', '1', '92', '362', '1', '2025-10-13 22:19:57');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('809', '1', '94', '365', '0', '2025-10-13 22:43:44');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('810', '1', '92', '361', '0', '2025-10-14 08:01:19');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('811', '1', '97', '373', '0', '2025-10-14 08:20:04');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('812', '1', '99', '377', '0', '2025-10-14 08:20:05');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('813', '1', '100', '381', '0', '2025-10-14 08:20:07');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('814', '1', '92', '362', '1', '2025-10-14 08:20:53');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('815', '1', '94', '367', '1', '2025-10-14 08:20:55');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('816', '2', '92', '362', '1', '2025-10-14 08:24:02');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('817', '2', '94', '367', '1', '2025-10-14 08:24:05');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('818', '2', '97', '375', '1', '2025-10-14 08:24:07');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('819', '2', '99', '378', '0', '2025-10-14 08:24:09');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('820', '2', '100', '383', '0', '2025-10-14 08:24:11');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('821', '2', '99', '379', '1', '2025-10-14 08:24:45');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('822', '2', '100', '382', '1', '2025-10-14 08:24:48');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('823', '2', '92', '362', '1', '2025-10-14 08:25:09');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('824', '2', '94', '367', '1', '2025-10-14 08:25:11');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('825', '2', '116', '446', '1', '2025-10-14 09:24:33');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('826', '1', '116', '445', '0', '2025-10-14 12:09:26');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('827', '1', '117', '449', '0', '2025-10-14 12:09:29');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('828', '2', '117', '449', '0', '2025-10-14 17:21:47');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('829', '2', '118', '454', '0', '2025-10-14 17:21:52');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('830', '1', '118', '454', '0', '2025-10-14 17:22:43');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('831', '1', '119', '458', '1', '2025-10-14 17:22:46');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('832', '1', '136', '526', '1', '2025-10-14 17:23:04');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('833', '1', '137', '530', '1', '2025-10-14 17:23:07');
INSERT INTO `respostas_usuario` (`id`, `user_id`, `id_questao`, `id_alternativa`, `acertou`, `data_resposta`) VALUES ('834', '2', '101', '385', '1', '2025-10-15 20:55:41');

--
-- Estrutura da tabela `respostas_usuarios`
--

DROP TABLE IF EXISTS `respostas_usuarios`;
CREATE TABLE `respostas_usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `id_questao` int(11) DEFAULT NULL,
  `acertou` tinyint(1) DEFAULT NULL,
  `data_resposta` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `id_questao` (`id_questao`),
  CONSTRAINT `respostas_usuarios_ibfk_1` FOREIGN KEY (`id_questao`) REFERENCES `questoes` (`id_questao`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `respostas_usuarios`
--

INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('36', '2', '92', '1', '2025-10-08 15:42:24');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('37', '2', '94', '1', '2025-10-08 15:42:27');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('38', '2', '97', '1', '2025-10-08 15:42:29');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('39', '2', '99', '1', '2025-10-08 15:42:56');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('40', '2', '92', '1', '2025-10-08 15:43:04');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('41', '2', '94', '1', '2025-10-08 15:43:06');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('42', '2', '97', '1', '2025-10-08 15:43:07');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('43', '2', '99', '1', '2025-10-08 15:43:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('44', '2', '100', '1', '2025-10-08 15:43:11');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('45', '2', '92', '1', '2025-10-08 15:43:33');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('46', '2', '94', '0', '2025-10-08 15:43:38');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('47', '1', '100', '1', '2025-10-08 15:45:00');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('48', '2', '92', '0', '2025-10-08 15:45:35');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('49', '2', '97', '0', '2025-10-08 15:45:36');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('50', '2', '99', '0', '2025-10-08 15:45:37');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('51', '2', '100', '0', '2025-10-08 15:45:39');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('52', '1', '92', '1', '2025-10-08 19:02:35');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('53', '1', '92', '0', '2025-10-08 19:02:49');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('54', '1', '92', '1', '2025-10-09 20:43:31');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('55', '1', '92', '1', '2025-10-09 20:44:55');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('56', '1', '94', '1', '2025-10-09 20:45:12');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('57', '1', '92', '0', '2025-10-09 20:45:23');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('58', '1', '94', '1', '2025-10-09 20:46:14');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('59', '1', '92', '1', '2025-10-09 21:15:12');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('60', '1', '94', '0', '2025-10-09 21:15:13');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('61', '1', '97', '0', '2025-10-09 21:15:14');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('62', '1', '94', '0', '2025-10-09 21:15:33');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('63', '1', '97', '0', '2025-10-09 21:15:34');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('64', '1', '94', '1', '2025-10-09 21:22:40');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('65', '2', '92', '1', '2025-10-10 12:16:26');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('66', '2', '94', '1', '2025-10-10 12:16:28');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('67', '2', '97', '1', '2025-10-10 12:16:30');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('68', '2', '99', '1', '2025-10-10 12:16:32');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('69', '2', '100', '1', '2025-10-10 12:16:36');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('70', '2', '100', '0', '2025-10-10 12:17:46');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('71', '2', '100', '0', '2025-10-10 17:40:58');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('72', '2', '100', '1', '2025-10-10 18:58:17');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('73', '2', '100', '0', '2025-10-10 19:42:45');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('74', '1', '100', '0', '2025-10-10 19:43:01');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('75', '1', '92', '1', '2025-10-12 10:54:57');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('76', '1', '94', '1', '2025-10-12 10:55:00');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('77', '1', '97', '1', '2025-10-12 10:55:02');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('78', '1', '99', '1', '2025-10-12 10:55:04');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('79', '2', '100', '0', '2025-10-12 10:56:27');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('80', '2', '92', '1', '2025-10-12 13:40:20');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('81', '1', '100', '1', '2025-10-12 13:41:51');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('82', '1', '100', '0', '2025-10-12 13:42:02');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('83', '1', '100', '0', '2025-10-12 13:42:16');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('84', '1', '100', '1', '2025-10-12 13:42:25');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('85', '1', '100', '0', '2025-10-12 14:06:32');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('86', '1', '100', '0', '2025-10-12 14:06:43');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('87', '1', '100', '0', '2025-10-12 14:07:00');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('88', '2', '94', '0', '2025-10-12 14:09:32');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('89', '2', '92', '0', '2025-10-12 14:09:40');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('90', '2', '92', '0', '2025-10-12 14:09:42');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('91', '2', '92', '0', '2025-10-12 14:09:51');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('92', '2', '92', '1', '2025-10-12 14:10:01');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('93', '2', '92', '0', '2025-10-12 14:10:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('94', '2', '92', '0', '2025-10-12 14:10:21');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('95', '2', '100', '0', '2025-10-12 14:17:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('96', '2', '100', '1', '2025-10-12 14:17:17');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('97', '2', '100', '0', '2025-10-12 14:17:24');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('98', '2', '100', '0', '2025-10-12 14:17:36');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('99', '2', '100', '0', '2025-10-12 14:17:57');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('100', '2', '100', '1', '2025-10-12 14:18:01');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('101', '2', '100', '1', '2025-10-12 14:18:13');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('102', '2', '100', '0', '2025-10-12 14:18:16');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('103', '2', '99', '0', '2025-10-12 14:18:27');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('104', '2', '99', '0', '2025-10-12 14:18:34');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('105', '2', '99', '0', '2025-10-12 14:18:42');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('106', '2', '99', '1', '2025-10-12 14:18:46');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('107', '2', '100', '0', '2025-10-12 14:30:40');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('108', '2', '100', '0', '2025-10-12 14:31:51');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('109', '2', '100', '0', '2025-10-12 14:31:58');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('110', '2', '92', '0', '2025-10-12 14:34:38');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('111', '2', '94', '1', '2025-10-12 14:34:40');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('112', '2', '97', '0', '2025-10-12 14:34:42');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('113', '2', '99', '1', '2025-10-12 14:34:44');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('114', '2', '100', '1', '2025-10-12 14:34:45');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('115', '1', '92', '1', '2025-10-12 17:54:53');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('116', '1', '92', '1', '2025-10-12 17:56:56');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('117', '3', '92', '1', '2025-10-12 20:45:34');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('118', '3', '94', '1', '2025-10-12 20:47:35');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('119', '3', '97', '1', '2025-10-12 20:48:29');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('120', '3', '99', '0', '2025-10-12 20:48:57');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('121', '3', '100', '1', '2025-10-12 20:49:10');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('122', '2', '94', '0', '2025-10-12 21:50:16');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('123', '3', '92', '1', '2025-10-12 21:51:41');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('124', '3', '94', '1', '2025-10-12 21:51:49');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('125', '3', '97', '1', '2025-10-12 21:52:02');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('126', '1', '92', '0', '2025-10-12 21:59:18');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('127', '1', '92', '1', '2025-10-13 20:42:43');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('128', '1', '92', '0', '2025-10-13 20:45:08');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('129', '2', '92', '0', '2025-10-13 20:58:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('130', '2', '92', '0', '2025-10-13 20:58:24');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('131', '2', '92', '0', '2025-10-13 21:14:19');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('132', '2', '94', '0', '2025-10-13 21:14:28');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('133', '2', '92', '1', '2025-10-13 21:57:13');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('134', '2', '92', '0', '2025-10-13 22:00:44');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('135', '2', '99', '0', '2025-10-13 22:00:45');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('136', '2', '100', '0', '2025-10-13 22:00:46');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('137', '1', '92', '1', '2025-10-13 22:19:14');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('138', '1', '100', '1', '2025-10-13 22:19:17');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('139', '1', '92', '1', '2025-10-13 22:19:57');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('140', '1', '94', '0', '2025-10-13 22:43:44');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('141', '1', '92', '0', '2025-10-14 08:01:19');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('142', '1', '97', '0', '2025-10-14 08:20:04');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('143', '1', '99', '0', '2025-10-14 08:20:05');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('144', '1', '100', '0', '2025-10-14 08:20:07');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('145', '1', '92', '1', '2025-10-14 08:20:53');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('146', '1', '94', '1', '2025-10-14 08:20:55');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('147', '2', '92', '1', '2025-10-14 08:24:02');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('148', '2', '94', '1', '2025-10-14 08:24:05');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('149', '2', '97', '1', '2025-10-14 08:24:07');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('150', '2', '99', '0', '2025-10-14 08:24:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('151', '2', '100', '0', '2025-10-14 08:24:11');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('152', '2', '99', '1', '2025-10-14 08:24:45');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('153', '2', '100', '1', '2025-10-14 08:24:48');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('154', '2', '92', '1', '2025-10-14 08:25:09');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('155', '2', '94', '1', '2025-10-14 08:25:11');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('156', '2', '116', '1', '2025-10-14 09:24:33');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('157', '1', '116', '0', '2025-10-14 12:09:26');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('158', '1', '117', '0', '2025-10-14 12:09:29');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('159', '2', '117', '0', '2025-10-14 17:21:47');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('160', '2', '118', '0', '2025-10-14 17:21:52');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('161', '1', '118', '0', '2025-10-14 17:22:43');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('162', '1', '119', '1', '2025-10-14 17:22:46');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('163', '1', '136', '1', '2025-10-14 17:23:04');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('164', '1', '137', '1', '2025-10-14 17:23:07');
INSERT INTO `respostas_usuarios` (`id`, `id_usuario`, `id_questao`, `acertou`, `data_resposta`) VALUES ('165', '2', '101', '1', '2025-10-15 20:55:41');

--
-- Estrutura da tabela `resultados`
--

DROP TABLE IF EXISTS `resultados`;
CREATE TABLE `resultados` (
  `id_resultado` int(11) NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) DEFAULT NULL,
  `id_assunto` int(11) DEFAULT NULL,
  `pontuacao` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `detalhes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`detalhes`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_resultado`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_assunto` (`id_assunto`),
  CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL,
  CONSTRAINT `resultados_ibfk_2` FOREIGN KEY (`id_assunto`) REFERENCES `assuntos` (`id_assunto`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Estrutura da tabela `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `data_criacao` datetime DEFAULT current_timestamp(),
  `tipo` varchar(50) NOT NULL,
  `ultimo_login` timestamp NULL DEFAULT NULL,
  `google_id` varchar(255) DEFAULT NULL,
  `avatar_url` varchar(512) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `google_id` (`google_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dados da tabela `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nome`, `email`, `senha`, `data_criacao`, `tipo`, `ultimo_login`, `google_id`, `avatar_url`, `updated_at`) VALUES ('1', 'kaique lourran', 'hebertribeiro2222@gmail.com', '$2y$10$YzgQWQNG/NqP.FAW6AMveOG6zoHrnpc6Uj4JiskiTkkhxKNpWwfPG', '2025-09-22 20:47:04', 'usuario', '2025-10-13 20:45:00', '107354506260753767586', 'https://lh3.googleusercontent.com/a/ACg8ocLYbRjbOr_qZWeHI4qECNNDqKB_oOIFWkzNOS7kCtD5SlEm3f2C=s96-c', '2025-10-13 20:45:00');
INSERT INTO `usuarios` (`id_usuario`, `nome`, `email`, `senha`, `data_criacao`, `tipo`, `ultimo_login`, `google_id`, `avatar_url`, `updated_at`) VALUES ('2', 'kaique lourran admin', 'kaiquenunis976@gmail.com', '$2y$10$pH76yKV.CV6d/ODySHrdiec.CVQR/OcWY6S9TCLIvJK9KkUCOVOs6', '2025-09-23 22:06:25', 'admin', '2025-10-15 00:17:25', '102133044997514768602', 'https://lh3.googleusercontent.com/a/ACg8ocLfAUEkmxz4H0UQvohS9GCJpjUJCnalGjY6RnAMFuq1vW_1N7NVzg=s96-c', '2025-10-15 00:17:25');
INSERT INTO `usuarios` (`id_usuario`, `nome`, `email`, `senha`, `data_criacao`, `tipo`, `ultimo_login`, `google_id`, `avatar_url`, `updated_at`) VALUES ('3', 'Cleice Vitória Santana Cruz', 'cleicevitoria02@gmail.com', '', '2025-10-12 20:42:11', '', NULL, '103072631544255699198', 'https://lh3.googleusercontent.com/a/ACg8ocIsPGcCBD9FrK_u8atBcdS1OK5Rho5U3XrWdybvqXJvK8oFpW0K_g=s96-c', '2025-10-12 21:21:39');

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
