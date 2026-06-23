# Knowledge Graph

_Generated 2026-04-24 from `domains/*.json`. Regenerate: `python3 build_graph.py`._

**Legend** — 🟢 mastered (≥ 0.7) · 🟡 learning (0 < m < 0.7) · ⚪ untouched (m = 0)

## Summary

| Domain | 🟢 | 🟡 | ⚪ | Total |
|---|---:|---:|---:|---:|
| CMSE 381 Exam 3 — Non-Linearity, Trees, SVM, Clustering | 0 | 2 | 12 | 14 |
| CMSE 404 Exam 3 — Non-Transformer Topics | 0 | 1 | 3 | 4 |
| Neural Networks (CMSE 381) | 6 | 1 | 8 | 15 |
| Encoder-Decoder Architecture (CMSE 404) | 6 | 5 | 9 | 20 |
| IAM & SSO Group Sync | 0 | 3 | 23 | 26 |
| Intro to AI | 2 | 2 | 12 | 16 |
| CNNs (CSE 440) | 4 | 1 | 11 | 16 |
| React Front-End Fundamentals | 0 | 0 | 27 | 27 |

## CMSE 381 Exam 3 — Non-Linearity, Trees, SVM, Clustering
_Goal: Master ISLP Ch 7-9, 12 for CMSE 381 Midterm 3 (2026-04-20). NN/CNN topics covered separately in data_science_methods_nn domain._

```mermaid
flowchart TD
    polynomial_regression["Polynomial Regression<br/>m=0.00"]
    step_functions["Step Functions<br/>m=0.00"]
    basis_functions["Basis Functions (General Framework)<br/>m=0.00"]
    piecewise_polynomials["Piecewise Polynomials & Knots<br/>m=0.00"]
    regression_splines["Regression Splines (Cubic & Natural)<br/>m=0.00"]
    decision_trees_381["Decision Trees (Regression & Classification)<br/>m=0.00"]
    tree_pruning["Tree Pruning & Cost-Complexity<br/>m=0.00"]
    bagging["Bagging (Bootstrap Aggregation)<br/>m=0.00"]
    random_forests["Random Forests<br/>m=0.20"]
    maximal_margin_classifier["Maximal Margin Classifier<br/>m=0.00"]
    support_vector_classifier["Support Vector Classifier (Soft Margin)<br/>m=0.00"]
    svm_kernels["SVM with Kernels (Polynomial, Radial)<br/>m=0.00"]
    kmeans_381["K-Means Clustering<br/>m=0.00"]
    hierarchical_clustering["Hierarchical Clustering<br/>m=0.20"]
    polynomial_regression --> basis_functions
    step_functions --> basis_functions
    basis_functions --> piecewise_polynomials
    piecewise_polynomials --> regression_splines
    decision_trees_381 --> tree_pruning
    decision_trees_381 --> bagging
    bagging --> random_forests
    maximal_margin_classifier --> support_vector_classifier
    support_vector_classifier --> svm_kernels

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class random_forests,hierarchical_clustering learning;
    class polynomial_regression,step_functions,basis_functions,piecewise_polynomials,regression_splines,decision_trees_381,tree_pruning,bagging,maximal_margin_classifier,support_vector_classifier,svm_kernels,kmeans_381 untouched;
```

## CMSE 404 Exam 3 — Non-Transformer Topics
_Goal: Master Decision Trees, Naive Bayes, Clustering, Pretrained LMs for CMSE 404 Exam 3 (2026-04-09)_

```mermaid
flowchart TD
    decision_trees["Decision Trees<br/>m=0.00"]
    naive_bayes["Naive Bayes<br/>m=0.00"]
    kmeans_clustering["K-Means Clustering<br/>m=0.00"]
    pretrained_language_models["Pretrained Language Models<br/>m=0.20"]

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class pretrained_language_models learning;
    class decision_trees,naive_bayes,kmeans_clustering untouched;
```

## Neural Networks (CMSE 381)
_Goal: Master ISLP Chapter 10 for CMSE 381 Lectures 29-31_

```mermaid
flowchart TD
    activation_functions["Activation Functions (ReLU, Sigmoid)<br/>m=0.80"]
    nn_motivation_structure["NN Motivation & Structure<br/>m=0.80"]
    single_layer_nn["Single Layer Neural Networks<br/>m=0.80"]
    loss_functions_nn["Loss Functions (Squared Error, Cross-Entropy)<br/>m=0.80"]
    multilayer_nn["Multilayer Neural Networks<br/>m=0.80"]
    softmax_multiclass["Softmax & Multiclass Output<br/>m=0.80"]
    fitting_gradient_descent["Fitting NNs: Gradient Descent<br/>m=0.00"]
    backpropagation["Backpropagation<br/>m=0.00"]
    regularization_dropout["Regularization & Dropout<br/>m=0.00"]
    sgd_minibatches["SGD & Minibatches<br/>m=0.00"]
    convolution_layers["Convolution Layers<br/>m=0.40"]
    pooling_layers["Pooling Layers<br/>m=0.00"]
    cnn_architecture["CNN Architecture<br/>m=0.00"]
    data_augmentation_transfer["Data Augmentation & Transfer Learning<br/>m=0.00"]
    when_to_use_deep_learning["When to Use Deep Learning<br/>m=0.00"]
    activation_functions --> single_layer_nn
    nn_motivation_structure --> single_layer_nn
    nn_motivation_structure --> loss_functions_nn
    single_layer_nn --> multilayer_nn
    loss_functions_nn --> multilayer_nn
    loss_functions_nn --> softmax_multiclass
    single_layer_nn --> softmax_multiclass
    multilayer_nn --> fitting_gradient_descent
    fitting_gradient_descent --> backpropagation
    multilayer_nn --> regularization_dropout
    fitting_gradient_descent --> sgd_minibatches
    multilayer_nn --> convolution_layers
    convolution_layers --> pooling_layers
    convolution_layers --> cnn_architecture
    pooling_layers --> cnn_architecture
    cnn_architecture --> data_augmentation_transfer
    cnn_architecture --> when_to_use_deep_learning
    regularization_dropout --> when_to_use_deep_learning

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class activation_functions,nn_motivation_structure,single_layer_nn,loss_functions_nn,multilayer_nn,softmax_multiclass mastered;
    class convolution_layers learning;
    class fitting_gradient_descent,backpropagation,regularization_dropout,sgd_minibatches,pooling_layers,cnn_architecture,data_augmentation_transfer,when_to_use_deep_learning untouched;
```

## Encoder-Decoder Architecture (CMSE 404)
_Goal: Master encoder-decoder and transformer fundamentals for CMSE 404 Exam 3_

```mermaid
flowchart TD
    sequence_modeling_motivation["Sequence Modeling & Motivation<br/>m=0.80"]
    rnn_fundamentals["RNN Fundamentals<br/>m=0.80"]
    vanishing_exploding_gradients["Vanishing/Exploding Gradients in RNNs<br/>m=0.80"]
    lstm_cells["LSTM Cells<br/>m=0.70"]
    autoencoders_basic["Autoencoders (Basic)<br/>m=0.10"]
    gru_cells["GRU Cells<br/>m=0.00"]
    seq2seq_problem_framing["Sequence-to-Sequence Problem Framing<br/>m=0.00"]
    denoising_sparse_autoencoders["Denoising & Sparse Autoencoders<br/>m=0.00"]
    variational_autoencoders["Variational Autoencoders (VAE)<br/>m=0.00"]
    encoder_component["Encoder Component (Seq2Seq)<br/>m=0.00"]
    decoder_component["Decoder Component (Seq2Seq)<br/>m=0.00"]
    context_vector_bottleneck["Context Vector & Information Bottleneck<br/>m=0.70"]
    attention_mechanism["Attention Mechanism (Bahdanau/Luong)<br/>m=0.70"]
    self_attention["Self-Attention<br/>m=0.50"]
    multi_head_attention["Multi-Head Attention<br/>m=0.20"]
    positional_encoding["Positional Encoding<br/>m=0.20"]
    transformer_encoder_block["Transformer Encoder Block<br/>m=0.20"]
    transformer_decoder_block["Transformer Decoder Block<br/>m=0.00"]
    full_transformer_architecture["Full Transformer Architecture<br/>m=0.00"]
    encoder_decoder_applications["Encoder-Decoder Applications (Translation, Summarization)<br/>m=0.00"]
    rnn_fundamentals --> vanishing_exploding_gradients
    vanishing_exploding_gradients --> lstm_cells
    lstm_cells --> gru_cells
    lstm_cells --> seq2seq_problem_framing
    autoencoders_basic --> denoising_sparse_autoencoders
    autoencoders_basic --> variational_autoencoders
    seq2seq_problem_framing --> encoder_component
    encoder_component --> decoder_component
    encoder_component --> context_vector_bottleneck
    decoder_component --> context_vector_bottleneck
    context_vector_bottleneck --> attention_mechanism
    attention_mechanism --> self_attention
    self_attention --> multi_head_attention
    self_attention --> positional_encoding
    multi_head_attention --> transformer_encoder_block
    positional_encoding --> transformer_encoder_block
    transformer_encoder_block --> transformer_decoder_block
    transformer_encoder_block --> full_transformer_architecture
    transformer_decoder_block --> full_transformer_architecture
    full_transformer_architecture --> encoder_decoder_applications

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class sequence_modeling_motivation,rnn_fundamentals,vanishing_exploding_gradients,lstm_cells,context_vector_bottleneck,attention_mechanism mastered;
    class autoencoders_basic,self_attention,multi_head_attention,positional_encoding,transformer_encoder_block learning;
    class gru_cells,seq2seq_problem_framing,denoising_sparse_autoencoders,variational_autoencoders,encoder_component,decoder_component,transformer_decoder_block,full_transformer_architecture,encoder_decoder_applications untouched;
```

## IAM & SSO Group Sync
_Goal: Build conceptual foundation for the sso_group_sync project_

```mermaid
flowchart TD
    identity_provider["Identity Provider (IdP)<br/>m=0.55"]
    service_provider["Service Provider (SP)<br/>m=0.15"]
    principal["Principal<br/>m=0.00"]
    authn_vs_authz["Authentication vs Authorization<br/>m=0.05"]
    source_of_truth["Source of Truth<br/>m=0.00"]
    schema["Schema<br/>m=0.00"]
    entitlement["Entitlement<br/>m=0.00"]
    provisioning_deprovisioning["Provisioning & Deprovisioning<br/>m=0.00"]
    rbac["Role-Based Access Control (RBAC)<br/>m=0.00"]
    principle_of_least_privilege["Principle of Least Privilege<br/>m=0.00"]
    idempotency["Idempotency<br/>m=0.00"]
    polling_vs_webhooks["Polling vs Webhooks<br/>m=0.00"]
    attribute_mapping["Attribute Mapping<br/>m=0.00"]
    eventual_consistency["Eventual Consistency<br/>m=0.00"]
    saml["SAML (Security Assertion Markup Language)<br/>m=0.00"]
    oauth2["OAuth 2.0<br/>m=0.00"]
    scim["SCIM (System for Cross-domain Identity Management)<br/>m=0.00"]
    group_sprawl["Group Sprawl<br/>m=0.00"]
    identity_fragmentation["Identity Fragmentation<br/>m=0.00"]
    drift["Drift<br/>m=0.00"]
    orphaned_access["Orphaned Access<br/>m=0.00"]
    api_rate_limiting["API Rate Limiting<br/>m=0.00"]
    audit_trail["Audit Trail<br/>m=0.00"]
    oidc["OpenID Connect (OIDC)<br/>m=0.00"]
    reconciliation["Reconciliation<br/>m=0.00"]
    zero_trust["Zero Trust<br/>m=0.00"]
    principal --> entitlement
    identity_provider --> provisioning_deprovisioning
    service_provider --> provisioning_deprovisioning
    principal --> provisioning_deprovisioning
    principal --> rbac
    entitlement --> rbac
    entitlement --> principle_of_least_privilege
    schema --> attribute_mapping
    source_of_truth --> eventual_consistency
    authn_vs_authz --> saml
    identity_provider --> saml
    service_provider --> saml
    authn_vs_authz --> oauth2
    provisioning_deprovisioning --> scim
    schema --> scim
    attribute_mapping --> scim
    rbac --> group_sprawl
    provisioning_deprovisioning --> group_sprawl
    source_of_truth --> identity_fragmentation
    identity_provider --> identity_fragmentation
    source_of_truth --> drift
    eventual_consistency --> drift
    provisioning_deprovisioning --> orphaned_access
    principle_of_least_privilege --> orphaned_access
    polling_vs_webhooks --> api_rate_limiting
    entitlement --> audit_trail
    rbac --> audit_trail
    oauth2 --> oidc
    source_of_truth --> reconciliation
    idempotency --> reconciliation
    drift --> reconciliation
    scim --> reconciliation
    principle_of_least_privilege --> zero_trust
    authn_vs_authz --> zero_trust

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class identity_provider,service_provider,authn_vs_authz learning;
    class principal,source_of_truth,schema,entitlement,provisioning_deprovisioning,rbac,principle_of_least_privilege,idempotency,polling_vs_webhooks,attribute_mapping,eventual_consistency,saml,oauth2,scim,group_sprawl,identity_fragmentation,drift,orphaned_access,api_rate_limiting,audit_trail,oidc,reconciliation,zero_trust untouched;
```

## Intro to AI
_Goal: Final exam on 2026-05-01 — surface familiarity with all 13 topics in final_topics.md, confident on step-by-step computation_

```mermaid
flowchart TD
    search_basics["Uninformed Search (BFS/DFS/UCS)<br/>m=0.00"]
    probability_basics["Probability Basics (joint, conditional, marginal)<br/>m=0.00"]
    linear_algebra_basics["Linear Algebra for ML (dot products, matrix mul)<br/>m=0.00"]
    a_star_search["A* Search Traversal and Calculation<br/>m=0.60"]
    expectimax["Expectimax<br/>m=0.80"]
    mdps["MDPs (states, actions, rewards, discount)<br/>m=0.00"]
    mdp_values["Compute MDP Values (value iteration)<br/>m=0.00"]
    markov_stationary["Markov Stationary Distribution<br/>m=0.00"]
    joint_from_prior["Calculating Joint Values from Prior<br/>m=0.20"]
    supervised_vs_unsupervised["Supervised vs Unsupervised Learning<br/>m=0.00"]
    data_augmentation["Data Augmentation<br/>m=0.00"]
    minibatch_epoch["Mini-batch and Epoch<br/>m=0.00"]
    filter_output["Calculating CNN Filter Output Size<br/>m=0.80"]
    mlp_lr_computation["MLP and Logistic Regression Full Computation<br/>m=0.00"]
    ce_loss["Computing Cross-Entropy Loss<br/>m=0.00"]
    gan_objective["GAN Objective Function Conversion<br/>m=0.00"]
    search_basics --> a_star_search
    search_basics --> expectimax
    probability_basics --> mdps
    mdps --> mdp_values
    probability_basics --> markov_stationary
    probability_basics --> joint_from_prior
    supervised_vs_unsupervised --> data_augmentation
    supervised_vs_unsupervised --> minibatch_epoch
    linear_algebra_basics --> filter_output
    linear_algebra_basics --> mlp_lr_computation
    supervised_vs_unsupervised --> mlp_lr_computation
    probability_basics --> ce_loss
    ce_loss --> gan_objective
    mlp_lr_computation --> gan_objective

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class expectimax,filter_output mastered;
    class a_star_search,joint_from_prior learning;
    class search_basics,probability_basics,linear_algebra_basics,mdps,mdp_values,markov_stationary,supervised_vs_unsupervised,data_augmentation,minibatch_epoch,mlp_lr_computation,ce_loss,gan_objective untouched;
```

## CNNs (CSE 440)
_Goal: Master CNNs for CSE 440 quiz (2026-04-09) and final exam (2026-05-01)_

```mermaid
flowchart TD
    convolution_operation["Convolution Operation (1D & 2D)<br/>m=0.70"]
    filters_kernels["Filters & Kernels (Box, Gaussian, Edge)<br/>m=0.00"]
    correlation_vs_convolution["Correlation vs. Convolution (Kernel Flip)<br/>m=0.00"]
    stride_padding["Stride, Padding & Output Size Formula<br/>m=0.70"]
    multichannel_convolution["Multi-Channel Convolution (RGB)<br/>m=0.10"]
    relu_activation["ReLU Activation in CNNs<br/>m=0.80"]
    pooling_layers_cse440["Pooling Layers (Max & Average)<br/>m=0.80"]
    cnn_layer_pipeline["CNN Layer Pipeline (Conv→ReLU→Pool→Norm→FC)<br/>m=0.00"]
    receptive_field["Receptive Field<br/>m=0.00"]
    weight_sharing["Weight Sharing & Parameter Counting<br/>m=0.00"]
    feature_hierarchy["Feature Hierarchy (Low→Mid→High Level)<br/>m=0.00"]
    dropout_cse440["Dropout Regularization<br/>m=0.00"]
    lenet5["LeNet-5 Architecture<br/>m=0.00"]
    alexnet["AlexNet Architecture & Details<br/>m=0.00"]
    vggnet["VGGNet (Small Filters, Deeper Networks)<br/>m=0.00"]
    transfer_learning_cse440["Transfer Learning & Fine-Tuning CNNs<br/>m=0.00"]
    convolution_operation --> correlation_vs_convolution
    filters_kernels --> correlation_vs_convolution
    convolution_operation --> stride_padding
    convolution_operation --> multichannel_convolution
    convolution_operation --> pooling_layers_cse440
    stride_padding --> cnn_layer_pipeline
    multichannel_convolution --> cnn_layer_pipeline
    relu_activation --> cnn_layer_pipeline
    pooling_layers_cse440 --> cnn_layer_pipeline
    stride_padding --> receptive_field
    multichannel_convolution --> weight_sharing
    stride_padding --> weight_sharing
    cnn_layer_pipeline --> feature_hierarchy
    cnn_layer_pipeline --> dropout_cse440
    cnn_layer_pipeline --> lenet5
    weight_sharing --> lenet5
    cnn_layer_pipeline --> alexnet
    weight_sharing --> alexnet
    dropout_cse440 --> alexnet
    alexnet --> vggnet
    receptive_field --> vggnet
    vggnet --> transfer_learning_cse440

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class convolution_operation,stride_padding,relu_activation,pooling_layers_cse440 mastered;
    class multichannel_convolution learning;
    class filters_kernels,correlation_vs_convolution,cnn_layer_pipeline,receptive_field,weight_sharing,feature_hierarchy,dropout_cse440,lenet5,alexnet,vggnet,transfer_learning_cse440 untouched;
```

## React Front-End Fundamentals
_Goal: Build a CRUD admin dashboard front-end for the sso_group_sync project (assumed scope; confirm with project owner). Includes JS/HTML/tooling prerequisites — Mark is at JS-zero per 2026-04-11 calibration._

```mermaid
flowchart TD
    html_basics["HTML Basics (tags, attributes, structure)<br/>m=0.00"]
    dom_model["The DOM (Document Object Model)<br/>m=0.00"]
    css_basics["CSS Basics (selectors, properties, classes)<br/>m=0.00"]
    js_variables["JS Variables (let, const, var, primitive types)<br/>m=0.00"]
    js_functions["JS Functions (declarations, arrow functions, return values)<br/>m=0.00"]
    js_arrays_objects["JS Arrays & Objects (literals, access, mutation)<br/>m=0.00"]
    js_destructuring["JS Destructuring (object and array)<br/>m=0.00"]
    js_array_methods["JS Array Methods (map, filter, reduce, forEach)<br/>m=0.00"]
    js_modules["JS Modules (import / export)<br/>m=0.00"]
    js_promises_async["JS Promises & async/await (concurrency, fetch)<br/>m=0.00"]
    html_forms["HTML Forms (input, select, button, labels)<br/>m=0.00"]
    node_npm_basics["Node & npm Basics (package.json, install, run)<br/>m=0.00"]
    jsx_syntax["JSX Syntax (expressions, attributes, fragments)<br/>m=0.00"]
    react_components["React Function Components<br/>m=0.00"]
    event_handling["Event Handling (onClick, onChange, handlers)<br/>m=0.00"]
    props["Props (passing data to components)<br/>m=0.00"]
    conditional_rendering["Conditional Rendering (&&, ternary, early return)<br/>m=0.00"]
    rendering_lists["Rendering Lists (.map and the key prop)<br/>m=0.00"]
    state_useState["State with useState (immutability, re-renders)<br/>m=0.00"]
    forms_controlled_components["Forms & Controlled Components (value + onChange)<br/>m=0.00"]
    state_lifting["Lifting State Up (parent-child data flow)<br/>m=0.00"]
    useEffect_basics["useEffect Basics (dependencies, cleanup, when effects run)<br/>m=0.00"]
    data_fetching_useEffect["Data Fetching in useEffect (loading, error, success)<br/>m=0.00"]
    component_structure["Component Structure (file organization, when to extract)<br/>m=0.00"]
    react_router_basics["React Router Basics (routes, links, params)<br/>m=0.00"]
    api_integration_pattern["API Integration Pattern (REST CRUD from React)<br/>m=0.00"]
    auth_gated_routes["Auth-Gated Routes (protected route pattern)<br/>m=0.00"]
    js_variables --> js_functions
    js_variables --> js_arrays_objects
    js_arrays_objects --> js_destructuring
    js_arrays_objects --> js_array_methods
    js_functions --> js_array_methods
    js_functions --> js_modules
    js_functions --> js_promises_async
    html_basics --> html_forms
    js_modules --> node_npm_basics
    html_basics --> jsx_syntax
    js_functions --> jsx_syntax
    js_variables --> jsx_syntax
    jsx_syntax --> react_components
    react_components --> event_handling
    js_functions --> event_handling
    react_components --> props
    js_destructuring --> props
    react_components --> conditional_rendering
    props --> rendering_lists
    js_array_methods --> rendering_lists
    react_components --> state_useState
    event_handling --> state_useState
    state_useState --> forms_controlled_components
    html_forms --> forms_controlled_components
    state_useState --> state_lifting
    props --> state_lifting
    state_useState --> useEffect_basics
    useEffect_basics --> data_fetching_useEffect
    js_promises_async --> data_fetching_useEffect
    props --> component_structure
    conditional_rendering --> component_structure
    react_components --> react_router_basics
    props --> react_router_basics
    data_fetching_useEffect --> api_integration_pattern
    react_router_basics --> auth_gated_routes
    state_useState --> auth_gated_routes

    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;
    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;
    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;
    class html_basics,dom_model,css_basics,js_variables,js_functions,js_arrays_objects,js_destructuring,js_array_methods,js_modules,js_promises_async,html_forms,node_npm_basics,jsx_syntax,react_components,event_handling,props,conditional_rendering,rendering_lists,state_useState,forms_controlled_components,state_lifting,useEffect_basics,data_fetching_useEffect,component_structure,react_router_basics,api_integration_pattern,auth_gated_routes untouched;
```
