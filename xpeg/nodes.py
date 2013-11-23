"""
AbstractNode(object)
  - node_name
  - matched_text
  - start
  - end
  - value

LeafNode(AbstractNode)  

Node(AbstractNode)
  - children[]

RulesNode(Node)
  RuleNode(Node)
    rule_name
    skip?
    ExpressionNode(Node)
      SequenceNodes(Node)
        SequenceNode(Node)
          PrefixNode(Node)
            LookaheadAssertionNode(Node)
              RegexNode(LeafNode)
            Suffix





"""