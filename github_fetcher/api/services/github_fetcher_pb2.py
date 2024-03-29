# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: github_fetcher.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14github_fetcher.proto\x12\x12stats.fetcher.grpc\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa9\x01\n\x14GithubFetcherRequest\x12\r\n\x05login\x18\x01 \x01(\t\x12\x33\n\ndate_start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\x31\n\x08\x64\x61te_end\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01\x88\x01\x01\x42\r\n\x0b_date_startB\x0b\n\t_date_end\"\xc3\x01\n\x15GithubFetcherResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05login\x18\x02 \x01(\t\x12\r\n\x05stars\x18\x03 \x01(\r\x12\x0f\n\x07\x63ommits\x18\x04 \x01(\r\x12\x15\n\rpull_requests\x18\x05 \x01(\r\x12\x0e\n\x06issues\x18\x06 \x01(\r\x12\x16\n\x0e\x63ontributed_to\x18\x07 \x01(\r\x12.\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp2p\n\rGithubFetcher\x12_\n\x08get_info\x12(.stats.fetcher.grpc.GithubFetcherRequest\x1a).stats.fetcher.grpc.GithubFetcherResponseb\x06proto3')



_GITHUBFETCHERREQUEST = DESCRIPTOR.message_types_by_name['GithubFetcherRequest']
_GITHUBFETCHERRESPONSE = DESCRIPTOR.message_types_by_name['GithubFetcherResponse']
GithubFetcherRequest = _reflection.GeneratedProtocolMessageType('GithubFetcherRequest', (_message.Message,), {
  'DESCRIPTOR' : _GITHUBFETCHERREQUEST,
  '__module__' : 'github_fetcher_pb2'
  # @@protoc_insertion_point(class_scope:stats.fetcher.grpc.GithubFetcherRequest)
  })
_sym_db.RegisterMessage(GithubFetcherRequest)

GithubFetcherResponse = _reflection.GeneratedProtocolMessageType('GithubFetcherResponse', (_message.Message,), {
  'DESCRIPTOR' : _GITHUBFETCHERRESPONSE,
  '__module__' : 'github_fetcher_pb2'
  # @@protoc_insertion_point(class_scope:stats.fetcher.grpc.GithubFetcherResponse)
  })
_sym_db.RegisterMessage(GithubFetcherResponse)

_GITHUBFETCHER = DESCRIPTOR.services_by_name['GithubFetcher']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GITHUBFETCHERREQUEST._serialized_start=78
  _GITHUBFETCHERREQUEST._serialized_end=247
  _GITHUBFETCHERRESPONSE._serialized_start=250
  _GITHUBFETCHERRESPONSE._serialized_end=445
  _GITHUBFETCHER._serialized_start=447
  _GITHUBFETCHER._serialized_end=559
# @@protoc_insertion_point(module_scope)
