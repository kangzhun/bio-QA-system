# -*- coding: utf-8 -*-

BIO_CYPER_TEMPLATE = {
    "node_property": "MATCH (node {name: '%s'}) RETURN node.%s",
    "equal_node_property": "MATCH (node {name: '%s'})-[r: 等同]-(equal_node) RETURN equal_node.%s",
    "all_node": "MATCH (node) RETURN node",
    "node_data": "MATCH (node {name: '%s'})-[]-(neighbors) RETURN node, neighbors",
    "neighbors_property": "MATCH (n {name: '%s'})-[r: %s]-(neighbors) RETURN neighbors.%s",
    "neighbors_data": "MATCH (n {name: '%s'})-[r: %s]-(neighbors) RETURN neighbors",
}
